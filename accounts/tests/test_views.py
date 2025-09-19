import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from unittest.mock import patch

User = get_user_model()

@pytest.mark.django_db
class TestAuthViews:

    def test_register_view_valid(self, client):
        data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "matric_number": "M1234567",
            "password": "securepass123",
            "confirm_password": "securepass123"
        }

        with patch("accounts.views.send_template_email") as mock_send:
            response = client.post(reverse("register"), data, follow=True)

        assert response.status_code == 200
        assert User.objects.filter(email="test@example.com").exists()
        user = User.objects.get(email="test@example.com")
        assert user.is_active is False
        messages = list(get_messages(response.wsgi_request))
        assert any("Please check your email" in m.message for m in messages)
        mock_send.assert_called_once()

    def test_login_invalid_user(self, client):
        response = client.post(reverse("login"), {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }, follow=True)

        messages = list(get_messages(response.wsgi_request))
        assert any("Invalid email or password." in m.message for m in messages)

    def test_login_inactive_user(self, client):
        user = User.objects.create_user(
            email="inactive@example.com",
            password="securepass",
            first_name="Test",
            last_name="User",
            matric_number="M0001"
        )
        response = client.post(reverse("login"), {
            "email": "inactive@example.com",
            "password": "securepass"
        }, follow=True)

        messages = list(get_messages(response.wsgi_request))
        assert any("Please activate your account" in m.message for m in messages)

    def test_logout_view(self, client):
        user = User.objects.create_user(
            email="user@example.com",
            password="pass",
            first_name="T",
            last_name="U",
            matric_number="M1000",
        )
        client.login(email="user@example.com", password="pass")
        response = client.get(reverse("logout"), follow=True)

        assert response.status_code == 200
        messages = list(get_messages(response.wsgi_request))
        assert any("logged out" in m.message.lower() for m in messages)

    def test_activate_account_success(self, client):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator

        user = User.objects.create_user(
            email="test@active.com",
            password="pass",
            first_name="X",
            last_name="Y",
            matric_number="M0000"
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        url = reverse("activate", kwargs={"uidb64": uid, "token": token})
        response = client.get(url, follow=True)

        user.refresh_from_db()
        assert user.is_active is True
        messages = list(get_messages(response.wsgi_request))
        assert any("account has been activated" in m.message.lower() for m in messages)

    def test_activate_account_invalid_token(self, client):
        user = User.objects.create_user(
            email="badtoken@example.com",
            password="pass",
            first_name="A",
            last_name="B",
            matric_number="M1001"
        )
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        url = reverse("activate", kwargs={"uidb64": uid, "token": "invalid-token"})
        response = client.get(url, follow=True)

        user.refresh_from_db()
        assert not user.is_active
        messages = list(get_messages(response.wsgi_request))
        assert any("invalid or has expired" in m.message.lower() for m in messages)
