from django.urls import resolve, reverse
from payments import views


def test_submit_payment_url_resolves():
    assert resolve(reverse('submit_payment')).func == views.submit_payment_view


def test_bank_transfer_url_resolves():
    assert resolve(reverse('bank_transfer_upload')).func == views.bank_transfer_upload_view


def test_paystack_url_resolves():
    assert resolve(reverse('paystack_payment')).func == views.paystack_payment_view


def test_callback_url_resolves():
    assert resolve(reverse('paystack_callback')).func == views.paystack_callback_view


def test_success_pages_resolve():
    assert resolve(reverse('payment_success')).func == views.payment_success_view
    assert resolve(reverse('bank_transfer_success')).func == views.bank_transfer_success_view
