import pytest
from django.core.exceptions import ValidationError
from accounts.models import User


@pytest.mark.django_db
class TestUserModel:

    def test_create_regular_user_successfully(self):
        user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            matric_number='ABC12345',
            password='securepassword123'
        )

        assert user.email == 'test@example.com'
        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert user.matric_number == 'ABC12345'
        assert user.is_active is False
        assert user.is_staff is False
        assert user.check_password('securepassword123')

    def test_create_superuser_successfully(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminsecurepass'
        )

        assert admin.email == 'admin@example.com'
        assert admin.first_name == 'Admin'
        assert admin.last_name == 'User'
        assert admin.matric_number == '0000000'
        assert admin.is_superuser is True
        assert admin.is_staff is True
        assert admin.check_password('adminsecurepass')

    def test_create_user_missing_email_raises_error(self):
        with pytest.raises(ValueError) as excinfo:
            User.objects.create_user(
                email='',
                first_name='Test',
                last_name='User',
                matric_number='ABC12345',
                password='pass'
            )
        assert "Users must have an email address" in str(excinfo.value)

    def test_create_user_missing_required_fields_raises_error(self):
        with pytest.raises(ValueError) as excinfo:
            User.objects.create_user(
                email='test@example.com',
                first_name='',
                last_name='',
                matric_number='',
                password='pass'
            )
        assert "First name, last name, and matric number are required" in str(excinfo.value)

    def test_user_str_returns_email(self):
        user = User(email='test@example.com')
        assert str(user) == 'test@example.com'
