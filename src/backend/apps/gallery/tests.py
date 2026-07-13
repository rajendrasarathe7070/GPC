"""Gallery tests."""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.gallery.models import Album


@pytest.mark.django_db
class TestGalleryAPI:
    def setup_method(self):
        self.client = APIClient()
        self.album = Album.objects.create(title="Annual Day", slug="annual-day", event_date="2024-03-15")

    def test_album_list(self):
        url = reverse("album-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

    def test_album_detail(self):
        url = reverse("album-detail", kwargs={"slug": self.album.slug})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["title"] == "Annual Day"
