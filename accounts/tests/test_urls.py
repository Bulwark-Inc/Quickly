from django.urls import reverse, resolve
from accounts.views import (
    login_view, logout_view, register_view,
    activate_account_view, resend_activation_email_view,
    forgot_password_view, reset_password_view
)


def test_login_url():
    assert reverse('login') == '/accounts/login/'
    assert resolve('/accounts/login/').func == login_view


def test_logout_url():
    assert reverse('logout') == '/accounts/logout/'
    assert resolve('/accounts/logout/').func == logout_view


def test_register_url():
    assert reverse('register') == '/accounts/register/'
    assert resolve('/accounts/register/').func == register_view


def test_activate_url():
    url = reverse('activate', kwargs={'uidb64': 'abc', 'token': '123'})
    assert url == '/accounts/activate/abc/123/'
    assert resolve('/accounts/activate/abc/123/').func == activate_account_view


def test_resend_activation_url():
    assert reverse('resend_activation') == '/accounts/resend-activation/'
    assert resolve('/accounts/resend-activation/').func == resend_activation_email_view


def test_forgot_password_url():
    assert reverse('forgot_password') == '/accounts/forgot-password/'
    assert resolve('/accounts/forgot-password/').func == forgot_password_view


def test_reset_password_url():
    url = reverse('reset_password', kwargs={'uidb64': 'abc', 'token': '123'})
    assert url == '/accounts/reset-password/abc/123/'
    assert resolve('/accounts/reset-password/abc/123/').func == reset_password_view
