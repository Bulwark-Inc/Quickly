from django.urls import resolve, reverse
from dashboard.views import dashboard_view

def test_dashboard_url_resolves():
    path = reverse('dashboard')
    assert resolve(path).func == dashboard_view
    assert path == '/dashboard/'
