"""Accounts module tests."""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.accounts.services import AuthService


@pytest.mark.django_db
class TestUserModel:
    def test_user_creation(self):
        user = User.objects.create_user(email="test@gpc.ac.in", password="TestPass123!", first_name="Test", last_name="User")
        assert user.email == "test@gpc.ac.in"
        assert user.check_password("TestPass123!")
        assert user.slug is not None

    def test_user_full_name(self):
        user = User.objects.create_user(email="test2@gpc.ac.in", password="TestPass123!", first_name="John", last_name="Doe")
        assert user.full_name == "John Doe"

    def test_user_is_locked(self):
        user = User.objects.create_user(email="locked@gpc.ac.in", password="TestPass123!", first_name="Locked", last_name="User")
        assert not user.is_locked


@pytest.mark.django_db
class TestAuthService:
    def test_register_success(self):
        user = AuthService.register(
            email="new@gpc.ac.in",
            password="SecurePass123!",
            first_name="New",
            last_name="User",
            role="student",
        )
        assert user is not None
        assert user.email == "new@gpc.ac.in"

    def test_register_duplicate_email(self):
        AuthService.register(email="dup@gpc.ac.in", password="SecurePass123!", first_name="Dup", last_name="User")
        with pytest.raises(Exception):
            AuthService.register(email="dup@gpc.ac.in", password="SecurePass123!", first_name="Dup", last_name="User")


@pytest.mark.django_db
class TestAuthAPI:
    def setup_method(self):
        self.client = APIClient()
        self.register_url = reverse("auth-register")
        self.login_url = reverse("auth-login")

    def test_register_api(self):
        payload = {
            "email": "api@gpc.ac.in",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
            "first_name": "API",
            "last_name": "Test",
            "role": "student",
        }
        response = self.client.post(self.register_url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True

    def test_login_api(self):
        User.objects.create_user(email="login@gpc.ac.in", password="SecurePass123!", first_name="Login", last_name="Test")
        payload = {"email": "login@gpc.ac.in", "password": "SecurePass123!"}
        response = self.client.post(self.login_url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data["data"]
        assert "refresh" in response.data["data"]

    def test_login_invalid_credentials(self):
        payload = {"email": "no@gpc.ac.in", "password": "wrong"}
        response = self.client.post(self.login_url, payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["success"] is False
