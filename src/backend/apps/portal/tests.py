"""Portal tests."""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestPortalViews:
    def setup_method(self):
        self.client = APIClient()

    def test_home_page(self):
        url = reverse("home")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_about_page(self):
        url = reverse("about")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_contact_page(self):
        url = reverse("contact-page")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_robots_txt(self):
        url = reverse("robots-txt")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert b"Sitemap:" in response.content
