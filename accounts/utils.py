from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


def generate_token_url(user, viewname, request, protocol=None):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    path = reverse(viewname, kwargs={'uidb64': uid, 'token': token})
    protocol = protocol or ('https' if not settings.DEBUG else 'http')
    domain = get_current_site(request).domain
    return f"{protocol}://{domain}{path}", uid, token


def send_template_email(subject, template_path, context, to_email, fail_silently=False):
    html_message = render_to_string(template_path, context)
    plain_message = strip_tags(html_message)  # fallback for plain-text clients

    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email]
    )
    email.attach_alternative(html_message, "text/html")
    try:
        email.send(fail_silently=fail_silently)
    except Exception as e:
        if not fail_silently:
            raise
        # Optionally log here
        print(f"Email sending failed: {e}")
