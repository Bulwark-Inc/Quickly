import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from payments.models import PaymentRecord, FeeType
from django.utils import timezone

User = get_user_model()


@pytest.mark.django_db
class TestDashboardView:

    def test_redirect_if_not_logged_in(self, client):
        response = client.get(reverse('dashboard'))
        assert response.status_code == 302
        assert '/accounts/login/' in response.url

    def test_dashboard_view_authenticated(self, client):
        # Create user
        user = User.objects.create_user(
            email="user@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            matric_number="M123"
        )
        user.is_active = True
        user.save()

        # Create FeeType and PaymentRecord
        fee_type = FeeType.objects.create(
            name="Tuition",
            amount=100000.00,
            charge=0.0
        )
        PaymentRecord.objects.create(
            user=user,
            fee_type=fee_type,
            total_amount=10000,
            amount_paid=10000,
            status='PAID',
            date_paid=timezone.now()
        )

        # Login and request dashboard
        client.login(email="user@example.com", password="password123")
        response = client.get(reverse('dashboard'))

        assert response.status_code == 200
        assert 'dashboard/dashboard.html' in [t.name for t in response.templates]
        assert 'payment_records' in response.context
        assert response.context['user'] == user
        assert len(response.context['payment_records']) == 1
