from django.urls import path
from .views import (
    register_view,
    login_view, logout_view, 
    activate_account_view, resend_activation_email_view, 
    forgot_password_view, reset_password_view
    )

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Register and Confirmation view
    path('register/', register_view, name='register'),
    path('activate/<uidb64>/<token>/', activate_account_view, name='activate'),
    
    # Password Reset URLs
    path('resend-activation/', resend_activation_email_view, name='resend_activation'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', reset_password_view, name='reset_password'),
]
