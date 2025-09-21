from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from payments.models import PaymentRecord
from .forms import ProfileUpdateForm
from django.conf import settings
import mimetypes
import os


@login_required
def view_receipt_secure(request, record_id):
    try:
        record = PaymentRecord.objects.get(pk=record_id)
    except PaymentRecord.DoesNotExist:
        raise Http404("Receipt not found")

    # Only the user who uploaded OR staff can view
    if record.user != request.user and not request.user.is_staff:
        raise Http404("You do not have permission to view this receipt")

    if not record.proof_of_payment:
        raise Http404("No receipt uploaded")

    file_path = record.proof_of_payment.path
    if not os.path.exists(file_path):
        raise Http404("File not found")

    mime_type, _ = mimetypes.guess_type(file_path)
    with open(file_path, 'rb') as f:
        return HttpResponse(f.read(), content_type=mime_type or 'application/octet-stream')


@login_required
def dashboard_view(request):
    user = request.user

    payment_records = PaymentRecord.objects.filter(user=user).select_related('fee_type').order_by('-date_paid')

    context = {
        "user": user,
        "payment_records": payment_records
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def update_profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'dashboard/update_profile.html', context)
