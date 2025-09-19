import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestHomeViews:

    def test_home_view(self, client):
        url = reverse('home')
        response = client.get(url)

        assert response.status_code == 200
        assert 'home/home.html' in [t.name for t in response.templates]

        # Test that key context data is passed to template
        expected_keys = ['features', 'about_bullets', 'overview_steps', 'testimonials']
        for key in expected_keys:
            assert key in response.context

    def test_about_view(self, client):
        url = reverse('about')
        response = client.get(url)

        assert response.status_code == 200
        assert 'home/about.html' in [t.name for t in response.templates]

    def test_contact_view(self, client):
        url = reverse('contact')
        response = client.get(url)

        assert response.status_code == 200
        assert 'home/contact.html' in [t.name for t in response.templates]
