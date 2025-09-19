import pytest
from accounts.utils import generate_token_url
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.core import mail
from accounts.models import User
from unittest.mock import patch


@pytest.mark.django_db
def test_generate_token_url(client):
    user = User.objects.create_user(
        email="tokentest@example.com",
        password="pass",
        first_name="Token",
        last_name="Tester",
        matric_number="M9876"
    )

    request = client.get("/").wsgi_request
    url, uid, token = generate_token_url(user, "activate", request)
    
    # Decode uid back and check
    from urllib.parse import urlparse

    parsed = urlparse(url)
    assert parsed.scheme in ["http", "https"]
    assert parsed.netloc == "testserver"

    assert url.endswith(f"/accounts/activate/{uid}/{token}/")

    decoded_uid = urlsafe_base64_decode(uid).decode()
    assert int(decoded_uid) == user.pk


@pytest.mark.django_db
@patch("accounts.utils.EmailMultiAlternatives.send")
def test_send_template_email_success(mock_send, settings):
    settings.DEFAULT_FROM_EMAIL = "no-reply@quickly.com"
    from accounts.utils import send_template_email

    user = User.objects.create_user(
        email="emailtest@example.com",
        password="pass",
        first_name="Email",
        last_name="Tester",
        matric_number="M123"
    )

    send_template_email(
        subject="Test Email",
        template_path="accounts/emails/activation_email.html",
        context={
            "user": user,
            "activation_url": "http://testserver/activate-link",
            "year": 2025
        },
        to_email=user.email
    )

    assert mock_send.called
