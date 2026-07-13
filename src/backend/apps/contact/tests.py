"""Contact tests."""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestContactAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_enquiry_create(self):
        url = reverse("enquiry-create")
        payload = {"name": "John", "email": "john@example.com", "subject": "Admission", "message": "How to apply?"}
        response = self.client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True

    def test_feedback_create(self):
        url = reverse("feedback-create")
        payload = {"name": "Jane", "email": "jane@example.com", "rating": 5, "comment": "Great college!"}
        response = self.client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
