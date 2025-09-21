from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PaymentRecord, PaymentSession, FeeType
from .forms import MultiFeePaymentForm, BankTransferProofForm
from django.conf import settings
import uuid
import requests
from django.views.decorators.csrf import csrf_exempt
from .utils import send_payment_email
from .pricing import calculate_adjusted_charge


@login_required
def submit_payment_view(request):
    user = request.user
    paid_fee_ids = PaymentRecord.objects.filter(user=user).values_list('fee_type_id', flat=True)
    selected_fee_ids = []

    if request.method == 'POST':
        form = MultiFeePaymentForm(request.POST)
        selected_fee_ids = request.POST.getlist('fee_types')

        if form.is_valid():
            fee_types = form.cleaned_data['fee_types']
            payment_method = form.cleaned_data['payment_method']

            duplicate_fees = [fee.name for fee in fee_types if fee.id in paid_fee_ids]
            if duplicate_fees:
                messages.warning(request, f"You've already paid for: {', '.join(duplicate_fees)}. Please uncheck those fees.")
                return render(request, 'payments/payment_list.html', {
                    'form': form,
                    'paid_fee_ids': list(paid_fee_ids),
                    'selected_fee_ids': selected_fee_ids,
                })

            total_amount = sum(fee.amount for fee in fee_types)  # sum of base amounts (without charges)
            base_charge = sum(fee.charge for fee in fee_types)  # sum of base charges before adjustment

            # Calculate adjusted charge using pricing rules
            adjusted_charge = calculate_adjusted_charge(total_amount, len(fee_types), base_charge)

            # Final total amount = total_amount + adjusted_charge
            final_total = total_amount + adjusted_charge

            session = PaymentSession.objects.create(
                user=user,
                payment_method=payment_method,
                total_amount=final_total
            )

            # Save adjusted charge info in session or somewhere if needed (optional)
            request.session['selected_fees'] = [fee.id for fee in fee_types]
            request.session['session_id'] = str(session.session_id)

            if payment_method == 'paystack':
                return redirect('paystack_payment')
            else:
                return redirect('bank_transfer_upload')

    else:
        form = MultiFeePaymentForm()

    return render(request, 'payments/payment_list.html', {
        'form': form,
        'paid_fee_ids': list(paid_fee_ids),
        'selected_fee_ids': selected_fee_ids,
    })


@login_required
def bank_transfer_upload_view(request):
    user = request.user
    selected_fee_ids = request.session.get('selected_fees')
    session_id = request.session.get('session_id')

    if not selected_fee_ids or not session_id:
        messages.error(request, "Session expired or invalid. Please start the payment process again.")
        return redirect('submit_payment')

    fees = FeeType.objects.filter(id__in=selected_fee_ids)
    try:
        session = PaymentSession.objects.get(session_id=session_id)
    except PaymentSession.DoesNotExist:
        messages.error(request, "Payment session not found.")
        return redirect('submit_payment')

    if request.method == 'POST':
        form = BankTransferProofForm(request.POST, request.FILES)
        if form.is_valid():
            proof = form.cleaned_data['proof_of_payment']

            for fee in fees:
                PaymentRecord.objects.create(
                    user=user,
                    fee_type=fee,
                    amount_paid=fee.amount,
                    charge=fee.charge,
                    total_amount=fee.total,
                    session=session,
                    proof_of_payment=proof,
                    status=PaymentRecord.STATUS_PENDING
                )

            messages.success(request, f"Payment submitted for {fees.count()} fee(s). Pending verification.")
            send_payment_email(user, session, fees, "bank transfer")

            # Clear session data after submission
            request.session.pop('selected_fees', None)
            request.session.pop('session_id', None)

            return redirect('bank_transfer_success')  # <-- Updated redirect

    else:
        form = BankTransferProofForm()

    return render(request, 'payments/bank_transfer.html', {
        'form': form,
        'fees': fees,
        'session': session,
    })


@login_required
def paystack_payment_view(request):
    user = request.user
    selected_fee_ids = request.session.get('selected_fees')
    session_id = request.session.get('session_id')

    if not selected_fee_ids or not session_id:
        messages.error(request, "Session expired or invalid. Please start the payment process again.")
        return redirect('submit_payment')

    fees = FeeType.objects.filter(id__in=selected_fee_ids)
    try:
        session = PaymentSession.objects.get(session_id=session_id)
    except PaymentSession.DoesNotExist:
        messages.error(request, "Payment session not found.")
        return redirect('submit_payment')

    amount_in_kobo = int(session.total_amount * 100)  # Paystack expects amount in kobo

    # Generate unique reference for Paystack
    reference = str(uuid.uuid4())
    session.paystack_reference = reference
    session.save()

    context = {
        'fees': fees,
        'session': session,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        'amount': amount_in_kobo,
        'email': user.email,
        'reference': reference,
        'callback_url': settings.PAYSTACK_CALLBACK_URL,
    }

    return render(request, 'payments/paystack_payment.html', context)


@login_required
@csrf_exempt
def paystack_callback_view(request):
    reference = request.GET.get('reference')
    if not reference:
        messages.error(request, "No payment reference provided.")
        return redirect('submit_payment')

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
    except (requests.RequestException, ValueError) as e:
        messages.error(request, "Could not verify payment at this time. Please try again later.")
        # Optionally log error: logger.exception(e)
        return redirect('submit_payment')


    if result['status'] and result['data']['status'] == 'success':
        try:
            session = PaymentSession.objects.get(paystack_reference=reference)
        except PaymentSession.DoesNotExist:
            messages.error(request, "Session not found for this payment.")
            return redirect('submit_payment')

        user = session.user
        fees = FeeType.objects.filter(id__in=request.session.get('selected_fees', []))

        # === DEMO MODE: Skip actual creation ===
        """
        for fee in fees:
            PaymentRecord.objects.create(
                user=user,
                fee_type=fee,
                amount_paid=fee.amount,
                charge=fee.charge,
                total_amount=fee.total,
                session=session,
                status=PaymentRecord.STATUS_VERIFIED
            )
        """

        send_payment_email(user, session, fees, "paystack")
        messages.success(request, f"[DEMO] Payment verified for {fees.count()} fee(s), but no records were created.")

        # Clear session
        request.session.pop('selected_fees', None)
        request.session.pop('session_id', None)

        return redirect('payment_success')
    else:
        messages.error(request, "Payment verification failed.")
        return redirect('submit_payment')


@login_required
def payment_success_view(request):
    return render(request, 'payments/payment_success.html')


@login_required
def bank_transfer_success_view(request):
    return render(request, 'payments/bank_transfer_success.html')