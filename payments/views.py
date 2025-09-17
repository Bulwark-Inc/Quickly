from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PaymentRecord, PaymentSession, FeeType
from .forms import MultiFeePaymentForm, BankTransferProofForm
from django.conf import settings


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

            total_amount = sum(fee.total for fee in fee_types)
            session = PaymentSession.objects.create(
                user=user,
                payment_method=payment_method,
                total_amount=total_amount
            )

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

    if request.method == 'POST':
        # Simulate payment success
        for fee in fees:
            PaymentRecord.objects.create(
                user=user,
                fee_type=fee,
                amount_paid=fee.amount,
                charge=fee.charge,
                total_amount=fee.total,
                session=session,
                status=PaymentRecord.STATUS_VERIFIED  # Instant verification
            )

        messages.success(request, f"Payment completed for {fees.count()} fee(s).")

        # Clear session data after successful payment
        request.session.pop('selected_fees', None)
        request.session.pop('session_id', None)

        return redirect('payment_success')  # <-- Updated redirect

    return render(request, 'payments/paystack_payment.html', {
        'fees': fees,
        'session': session,
    })


@login_required
def payment_success_view(request):
    return render(request, 'payments/payment_success.html')


@login_required
def bank_transfer_success_view(request):
    return render(request, 'payments/bank_transfer_success.html')