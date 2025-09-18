from django.urls import path
from .views import (
    submit_payment_view, 
    bank_transfer_upload_view, paystack_payment_view,
    paystack_callback_view,
    payment_success_view, bank_transfer_success_view
)

urlpatterns = [
    path('', submit_payment_view, name='submit_payment'),
    path('bank-transfer/', bank_transfer_upload_view, name='bank_transfer_upload'),
    path('paystack/', paystack_payment_view, name='paystack_payment'),
    path('paystack/callback/', paystack_callback_view, name='paystack_callback'),
    path('bank-transfer-success/', bank_transfer_success_view, name='bank_transfer_success'),
    path('payment-success/', payment_success_view, name='payment_success'),
]