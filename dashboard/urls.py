from django.urls import path
from .views import dashboard_view, view_receipt_secure

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('receipt/<int:record_id>/', view_receipt_secure, name='view_receipt_secure'),
]