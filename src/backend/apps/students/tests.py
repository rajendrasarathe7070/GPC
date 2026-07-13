"""Students tests."""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.academics.models import Course, Department
from apps.students.models import StudentProfile


@pytest.mark.django_db
class TestStudentProfileAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="student@gpc.ac.in", password="TestPass123!", first_name="Student", last_name="Test")
        dept = Department.objects.create(name="Mech", code="ME")
        course = Course.objects.create(name="Mechanical", code="ME101", department=dept)
        self.profile = StudentProfile.objects.create(
            user=self.user,
            enrollment_number="ENR20240001",
            roll_number="R001",
            course=course,
            admission_date="2024-06-01",
        )
        self.client.force_authenticate(user=self.user)

    def test_student_profile_get(self):
        url = reverse("student-profile")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["enrollment_number"] == "ENR20240001"
