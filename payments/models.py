import uuid
from django.db import models
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator


def user_directory_path(instance, filename):
    return f'payment_proofs/user_{instance.user.id}/{filename}'

class FeeType(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Your admin/service charge")
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.amount = self.amount or 0.0
        self.charge = self.charge or 0.0
        self.total = self.amount + self.charge
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - ₦{self.total} (₦{self.amount} + ₦{self.charge})"


class PaymentSession(models.Model):
    METHOD_PAYSTACK = 'paystack'
    METHOD_BANK_TRANSFER = 'bank_transfer'

    PAYMENT_METHOD_CHOICES = [
        (METHOD_PAYSTACK, 'Paystack'),
        (METHOD_BANK_TRANSFER, 'Bank Transfer'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    paystack_reference = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Session {self.session_id} - {self.user.email} - ₦{self.total_amount}"


class PaymentRecord(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_VERIFIED = 'verified'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_VERIFIED, 'Verified'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    session = models.ForeignKey(PaymentSession, on_delete=models.SET_NULL, null=True, blank=True)
    proof_of_payment = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.fee_type.name} - ₦{self.amount_paid}"


class PricingRule(models.Model):
    """Defines a pricing condition and what charge/discount to apply."""
    
    RULE_TYPE_FLAT = 'flat'
    RULE_TYPE_PERCENT = 'percent'

    RULE_TYPE_CHOICES = [
        (RULE_TYPE_FLAT, 'Flat Fee'),
        (RULE_TYPE_PERCENT, 'Percentage Discount'),
    ]

    min_total_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Minimum total amount (inclusive) for this rule to apply"
    )
    max_total_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Maximum total amount (inclusive) for this rule to apply"
    )
    min_fee_count = models.PositiveIntegerField(default=1, help_text="Minimum number of selected fees")
    max_fee_count = models.PositiveIntegerField(default=10, help_text="Maximum number of selected fees")

    rule_type = models.CharField(max_length=10, choices=RULE_TYPE_CHOICES)
    value = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Flat fee (₦) or percent (e.g., enter 20 for 20%) depending on rule type"
    )

    description = models.TextField(blank=True, help_text="Optional description of the rule")

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['min_total_amount', 'min_fee_count']

    def __str__(self):
        return f"{self.get_rule_type_display()} rule: ₦{self.min_total_amount}–₦{self.max_total_amount}, {self.min_fee_count}–{self.max_fee_count} fees"

    def applies_to(self, total_amount: Decimal, fee_count: int) -> bool:
        return (
            self.is_active and
            self.min_total_amount <= total_amount <= self.max_total_amount and
            self.min_fee_count <= fee_count <= self.max_fee_count
        )
