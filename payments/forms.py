from django import forms
from .models import FeeType, PaymentRecord, PaymentSession


class PaymentRecordForm(forms.ModelForm):
    class Meta:
        model = PaymentRecord
        fields = ['fee_type', 'proof_of_payment']  # Removed 'amount_paid' as requested
        widgets = {
            'fee_type': forms.Select(attrs={'class': 'form-control'}),
            'proof_of_payment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_proof_of_payment(self):
        file = self.cleaned_data.get('proof_of_payment')
        if file:
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File too large. Max size is 5MB.")
            if file.content_type not in ['application/pdf', 'image/jpeg', 'image/png']:
                raise forms.ValidationError("Unsupported file type. Only PDF, JPG, and PNG are allowed.")
        return file


class MultiFeePaymentForm(forms.Form):
    fee_types = forms.ModelMultipleChoiceField(
        queryset=FeeType.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Fee(s) to Pay"
    )
    payment_method = forms.ChoiceField(
        choices=PaymentSession.PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Payment Method"
    )

class BankTransferProofForm(forms.Form):
    proof_of_payment = forms.FileField(
        required=True,
        help_text="Upload PDF, JPG, or PNG (Max 5MB).",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label="Proof of Payment"
    )

    def clean_proof_of_payment(self):
        file = self.cleaned_data.get('proof_of_payment')
        if file:
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File too large. Max size is 5MB.")
            if file.content_type not in ['application/pdf', 'image/jpeg', 'image/png']:
                raise forms.ValidationError("Unsupported file type. Only PDF, JPG, and PNG are allowed.")
        return file