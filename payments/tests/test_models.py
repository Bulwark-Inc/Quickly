import pytest
from payments.models import FeeType, PaymentSession, PaymentRecord
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


@pytest.mark.django_db
def test_fee_type_total_calculation():
    fee = FeeType.objects.create(name="Test Fee", amount=Decimal('1000.00'), charge=Decimal('200.00'))
    assert fee.total == Decimal('1200.00')
    assert str(fee) == "Test Fee - ₦1200.00 (₦1000.00 + ₦200.00)"


@pytest.mark.django_db
def test_payment_session_str():
    user = User.objects.create_user(email="test@example.com", password="pass")
    session = PaymentSession.objects.create(user=user, payment_method='paystack', total_amount=Decimal('1500.00'))
    assert str(session).startswith("Session")
    assert str(session).endswith(f"{user.email} - ₦1500.00")


@pytest.mark.django_db
def test_payment_record_str():
    user = User.objects.create_user(email="test@example.com", password="pass")
    fee = FeeType.objects.create(name="Mock Fee", amount=Decimal('1000.00'), charge=Decimal('0.00'))
    record = PaymentRecord.objects.create(
        user=user,
        fee_type=fee,
        amount_paid=fee.amount,
        total_amount=fee.amount,
        status=PaymentRecord.STATUS_PENDING
    )
    assert str(record) == "test@example.com - Mock Fee - ₦1000.00"
