import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from payments.forms import BankTransferProofForm, MultiFeePaymentForm
from payments.models import FeeType, PaymentSession


@pytest.mark.django_db
def test_bank_transfer_form_valid_pdf():
    file = SimpleUploadedFile("proof.pdf", b"dummy content", content_type="application/pdf")
    form = BankTransferProofForm(files={'proof_of_payment': file})
    assert form.is_valid()


@pytest.mark.django_db
def test_bank_transfer_form_rejects_large_file():
    file = SimpleUploadedFile("big.pdf", b"a" * (6 * 1024 * 1024), content_type="application/pdf")
    form = BankTransferProofForm(files={'proof_of_payment': file})
    assert not form.is_valid()
    assert "File too large" in str(form.errors)


@pytest.mark.django_db
def test_multifee_payment_form():
    fee1 = FeeType.objects.create(name="Fee1", amount=100, charge=10)
    form_data = {
        'fee_types': [fee1.pk],
        'payment_method': PaymentSession.METHOD_PAYSTACK
    }
    form = MultiFeePaymentForm(data=form_data)
    assert form.is_valid()
