"""Faculty tests."""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.academics.models import Department
from apps.faculty.models import FacultyProfile


@pytest.mark.django_db
class TestFacultyAPI:
    def setup_method(self):
        self.client = APIClient()
        dept = Department.objects.create(name="Electrical", code="EE")
        user = User.objects.create_user(email="faculty@gpc.ac.in", password="TestPass123!", first_name="Faculty", last_name="Test")
        self.faculty = FacultyProfile.objects.create(user=user, employee_id="EMP001", department=dept, joining_date="2020-01-01")

    def test_faculty_list(self):
        url = reverse("faculty-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

    def test_faculty_detail(self):
        url = reverse("faculty-detail", kwargs={"employee_id": self.faculty.employee_id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["employee_id"] == "EMP001"
