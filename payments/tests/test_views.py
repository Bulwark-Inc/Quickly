import pytest
from django.urls import reverse
from payments.models import FeeType, PaymentSession
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_submit_payment_view_renders_for_logged_in_user(client, django_user_model):
    user = django_user_model.objects.create_user(email="test@site.com", password="pass")
    client.login(email="test@site.com", password="pass")

    response = client.get(reverse('submit_payment'))
    assert response.status_code == 200
    assert 'payments/payment_list.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_bank_transfer_upload_redirects_if_session_invalid(client, django_user_model):
    user = django_user_model.objects.create_user(email="test@site.com", password="pass")
    client.login(email="test@site.com", password="pass")

    response = client.get(reverse('bank_transfer_upload'))
    assert response.status_code == 302
    assert reverse('submit_payment') in response.url


@pytest.mark.django_db
def test_payment_success_view(client, django_user_model):
    user = django_user_model.objects.create_user(email="test@site.com", password="pass")
    client.login(email="test@site.com", password="pass")

    response = client.get(reverse('payment_success'))
    assert response.status_code == 200
    assert 'payments/payment_success.html' in [t.name for t in response.templates]
