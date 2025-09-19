import pytest
from accounts.forms import (
    UserRegistrationForm,
    ResendActivationEmailForm,
    ForgotPasswordForm,
    ResetPasswordForm
)


@pytest.mark.django_db
class TestUserRegistrationForm:

    def test_valid_data(self):
        form = UserRegistrationForm(data={
            'email': 'user@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'matric_number': 'M1234567',
            'password': 'secret123',
            'confirm_password': 'secret123'
        })
        assert form.is_valid()

    def test_passwords_do_not_match(self):
        form = UserRegistrationForm(data={
            'email': 'user@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'matric_number': 'M1234567',
            'password': 'secret123',
            'confirm_password': 'wrongpass'
        })
        assert not form.is_valid()
        assert 'confirm_password' in form.errors
        assert form.errors['confirm_password'][0] == "Passwords do not match."


class TestResendActivationEmailForm:

    def test_valid_email(self):
        form = ResendActivationEmailForm(data={'email': 'user@example.com'})
        assert form.is_valid()

    def test_missing_email(self):
        form = ResendActivationEmailForm(data={})
        assert not form.is_valid()
        assert 'email' in form.errors


class TestForgotPasswordForm:

    def test_valid_email(self):
        form = ForgotPasswordForm(data={'email': 'user@example.com'})
        assert form.is_valid()

    def test_blank_email(self):
        form = ForgotPasswordForm(data={'email': ''})
        assert not form.is_valid()


class TestResetPasswordForm:

    def test_valid_passwords(self):
        form = ResetPasswordForm(data={
            'new_password': 'newsecret123',
            'confirm_password': 'newsecret123'
        })
        assert form.is_valid()

    def test_mismatched_passwords(self):
        form = ResetPasswordForm(data={
            'new_password': 'newsecret123',
            'confirm_password': 'wrongpass'
        })
        assert not form.is_valid()
        assert 'confirm_password' in form.errors
        assert form.errors['confirm_password'][0] == "Passwords do not match."
