from django.urls import path
from .views import dashboard_view, view_receipt_secure, update_profile_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('update-profile/', update_profile_view, name='update_profile'),
    path('receipt/<int:record_id>/', view_receipt_secure, name='view_receipt_secure'),
]