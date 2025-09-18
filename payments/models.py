import uuid
from django.db import models
from django.conf import settings


class FeeType(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Your admin/service charge")
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
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
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # What the user paid
    charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # amount + charge
    session = models.ForeignKey(PaymentSession, on_delete=models.SET_NULL, null=True, blank=True)
    proof_of_payment = models.FileField(upload_to='payment_proofs/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.fee_type.name} - ₦{self.amount_paid}"
