from django.urls import path
from .views import submit_payment_view, bank_transfer_upload_view, paystack_payment_view, payment_success_view, bank_transfer_success_view

urlpatterns = [
    path('', submit_payment_view, name='submit_payment'),
    path('paystack/', paystack_payment_view, name='paystack_payment'),
    path('bank-transfer/', bank_transfer_upload_view, name='bank_transfer_upload'),
    path('payment-success/', payment_success_view, name='payment_success'),
    path('bank-transfer-success/', bank_transfer_success_view, name='bank_transfer_success'),
]
