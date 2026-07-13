"""Academics tests."""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.academics.models import Department


@pytest.mark.django_db
class TestDepartmentAPI:
    def setup_method(self):
        self.client = APIClient()
        self.department = Department.objects.create(name="Computer Science", code="CS", description="CS Department")

    def test_department_list(self):
        url = reverse("department-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

    def test_department_detail(self):
        url = reverse("department-detail", kwargs={"slug": self.department.slug})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["name"] == "Computer Science"
