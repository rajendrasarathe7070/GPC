"""Events tests."""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.events.models import Event, EventCategoryModel


@pytest.mark.django_db
class TestEventAPI:
    def setup_method(self):
        self.client = APIClient()
        self.category = EventCategoryModel.objects.create(name="Tech", slug="tech")
        self.event = Event.objects.create(
            title="Hackathon",
            slug="hackathon",
            description="Annual hackathon event.",
            category=self.category,
            start_datetime="2025-01-01T09:00:00Z",
            end_datetime="2025-01-02T18:00:00Z",
            venue="Main Hall",
        )

    def test_event_list(self):
        url = reverse("event-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

    def test_event_detail(self):
        url = reverse("event-detail", kwargs={"slug": self.event.slug})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["title"] == "Hackathon"
