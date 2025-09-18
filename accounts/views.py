from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()

from .forms import (
    UserRegistrationForm,
    ResendActivationEmailForm,
    ForgotPasswordForm,
    ResetPasswordForm,
)
from .models import User
from .utils import generate_token_url, send_template_email


#-----------------------------------------------
# Authentication Views (login, logout, register)
#-----------------------------------------------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            activation_url, _, _ = generate_token_url(user, 'activate', request)

            send_template_email(
                subject="Activate your Quickly account",
                template_path="accounts/emails/activation_email.html",
                context={
                    "user": user,
                    "activation_url": activation_url,
                    "year": timezone.now().year,
                },
                to_email=user.email
            )

            messages.success(request, "Please check your email to confirm your registration.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    request.session.pop('unverified_user_email', None)

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                messages.error(request, "Please activate your account via the email we sent.")
                request.session['unverified_user_email'] = user.email
            elif not check_password(password, user.password):
                messages.error(request, "Invalid email or password.")
            else:
                login(request, user)
                messages.success(request, f"Welcome, {user.first_name}!")
                return redirect('dashboard')
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You’ve been logged out.")
    return redirect('login')


#----------------------------------
# Email Verification Views
#----------------------------------
def activate_account_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        return redirect('login')


def resend_activation_email_view(request):
    initial_data = {'email': request.GET.get('email')} if 'email' in request.GET else {}
    if request.method == 'POST':
        form = ResendActivationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    activation_url, _, _ = generate_token_url(user, 'activate', request)
                    send_template_email(
                        subject="Resend Activation Email",
                        template_path="accounts/emails/activation_email.html",
                        context={
                            "user": user,
                            "activation_url": activation_url,
                            "year": timezone.now().year,
                        },
                        to_email=user.email
                    )
                    messages.success(request, 'A new activation email has been sent.')
                    return redirect('login')
                else:
                    messages.info(request, 'This account is already active.')
            except User.DoesNotExist:
                messages.error(request, 'No account with this email was found.')
    else:
         form = ResendActivationEmailForm(initial=initial_data)
    
    return render(request, 'accounts/resend_activation.html', {'form': form})


def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email, is_active=True)
                reset_url, _, _ = generate_token_url(user, 'reset_password', request)
                send_template_email(
                    subject="Reset your Quickly password",
                    template_path="accounts/emails/password_reset_email.html",
                    context={
                        "user": user,
                        "reset_link": reset_url,
                        "year": timezone.now().year,
                    },
                    to_email=user.email
                )
                messages.success(request, "We've emailed you a password reset link.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "No active account found with that email.")
    else:
        form = ForgotPasswordForm()

    return render(request, 'accounts/forgot_password.html', {'form': form})


def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, 'Invalid or expired password reset link.')
        return redirect('login')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['new_password']
            user.set_password(password)
            user.save()
            messages.success(request, 'Your password has been reset. You can now log in.')
            return redirect('login')
    else:
        form = ResetPasswordForm()

    return render(request, 'accounts/reset_password.html', {'form': form})
