from django.core.mail import send_mail
from django.conf import settings

def send_payment_email(user, session, fees, method):
    fee_details = "\n".join([f"- {fee.name}: ₦{fee.total}" for fee in fees])
    subject = f"New Payment Submitted ({method.title()})"
    message = f"""
        Hi,

        A new payment has been submitted by {user.first_name} ({user.email}).

        Payment Method: {method.title()}
        Total Amount: ₦{session.total_amount}

        Fees Paid:
        {fee_details}

        Session ID: {session.session_id}

        Best regards,
        Quickly team.
        """.strip()

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.EMAIL_HOST_USER],  # You can change this to another admin email
        fail_silently=False
    )
