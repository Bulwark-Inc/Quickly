from django.urls import resolve, reverse
from home.views import home_view, about_view, contact_view


def test_home_url_resolves():
    path = reverse('home')
    assert resolve(path).func == home_view
    assert path == '/'


def test_about_url_resolves():
    path = reverse('about')
    assert resolve(path).func == about_view
    assert path == '/about/'


def test_contact_url_resolves():
    path = reverse('contact')
    assert resolve(path).func == contact_view
    assert path == '/contact/'
