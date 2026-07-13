"""Accounts API views."""

import logging

from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import ActivityLog, AuditLog, UserSession
from apps.accounts.serializers import (
    ActivityLogSerializer,
    AuditLogSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    TokenResponseSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    UserSessionSerializer,
)
from apps.accounts.services import AuthService, UserService
from shared.exceptions import GPCException
from shared.utils.pagination import StandardResultsSetPagination
from shared.utils.response import error_response, success_response

logger = logging.getLogger("gpc")


class RegisterView(APIView):
    """User registration endpoint."""

    permission_classes = [AllowAny]

    @ratelimit(key="ip", rate="3/h", method="POST", block=True)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Registration failed.",
                code="validation_error",
                errors=serializer.errors,
            )
        try:
            user = serializer.save()
            return success_response(
                data=UserSerializer(user).data,
                message="Registration successful. Please verify your email.",
                status_code=status.HTTP_201_CREATED,
            )
        except GPCException as exc:
            return error_response(message=exc.message, code=exc.code, status_code=exc.status_code)
        except Exception as exc:
            logger.exception("Registration error")
            return error_response(
                message="Registration failed. Please try again later.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(APIView):
    """User login endpoint returning JWT tokens."""

    permission_classes = [AllowAny]

    @ratelimit(key="ip", rate="5/m", method="POST", block=True)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Invalid input.",
                code="validation_error",
                errors=serializer.errors,
            )
        try:
            result = AuthService.login(request, **serializer.validated_data)
            return success_response(
                data=TokenResponseSerializer(result).data,
                message="Login successful.",
            )
        except GPCException as exc:
            return error_response(message=exc.message, code=exc.code, status_code=exc.status_code)
        except Exception as exc:
            logger.exception("Login error")
            return error_response(
                message="Login failed. Please try again later.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LogoutView(APIView):
    """User logout endpoint blacklisting refresh token."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            AuthService.logout(request.user, refresh_token)
            return success_response(message="Logout successful.")
        except Exception as exc:
            logger.exception("Logout error")
            return error_response(
                message="Logout failed.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProfileView(APIView):
    """User profile retrieval and update."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = UserService.get_profile(request.user.id)
            return success_response(data=UserSerializer(user).data)
        except GPCException as exc:
            return error_response(message=exc.message, code=exc.code, status_code=exc.status_code)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(
                message="Update failed.",
                code="validation_error",
                errors=serializer.errors,
            )
        try:
            user = UserService.update_profile(request.user.id, **serializer.validated_data)
            return success_response(data=UserSerializer(user).data, message="Profile updated successfully.")
        except GPCException as exc:
            return error_response(message=exc.message, code=exc.code, status_code=exc.status_code)
        except Exception as exc:
            logger.exception("Profile update error")
            return error_response(
                message="Profile update failed.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PasswordChangeView(APIView):
    """Password change endpoint."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                code="validation_error",
                errors=serializer.errors,
            )
        try:
            AuthService.change_password(
                request.user,
                serializer.validated_data["old_password"],
                serializer.validated_data["new_password"],
            )
            return success_response(message="Password changed successfully.")
        except GPCException as exc:
            return error_response(message=exc.message, code=exc.code, status_code=exc.status_code)
        except Exception as exc:
            logger.exception("Password change error")
            return error_response(
                message="Password change failed.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PasswordResetRequestView(APIView):
    """Request password reset email."""

    permission_classes = [AllowAny]

    @ratelimit(key="ip", rate="3/h", method="POST", block=True)
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Invalid input.",
                code="validation_error",
                errors=serializer.errors,
            )
        try:
            AuthService.request_password_reset(serializer.validated_data["email"])
            return success_response(
                message="If an account exists with this email, you will receive a password reset link.",
            )
        except Exception as exc:
            logger.exception("Password reset request error")
            return error_response(
                message="Request failed. Please try again later.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PasswordResetConfirmView(APIView):
    """Confirm password reset with token."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Invalid input.",
                code="validation_error",
                errors=serializer.errors,
            )
        try:
            AuthService.reset_password(
                serializer.validated_data["token"],
                serializer.validated_data["new_password"],
            )
            return success_response(message="Password reset successful. Please log in with your new password.")
        except GPCException as exc:
            return error_response(message=exc.message, code=exc.code, status_code=exc.status_code)
        except Exception as exc:
            logger.exception("Password reset confirm error")
            return error_response(
                message="Password reset failed.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AuditLogListView(APIView):
    """List audit logs (Admin only)."""

    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        if not request.user.is_staff:
            return error_response(
                message="Permission denied.",
                code="permission_denied",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        logs = AuditLog.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(logs, request)
        serializer = AuditLogSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ActivityLogListView(APIView):
    """List current user's activity logs."""

    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        logs = ActivityLog.objects.filter(user=request.user)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(logs, request)
        serializer = ActivityLogSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class SessionListView(APIView):
    """List and manage user sessions."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = UserSession.objects.filter(user=request.user, is_active=True)
        serializer = UserSessionSerializer(sessions, many=True)
        return success_response(data=serializer.data)

    def delete(self, request):
        session_id = request.data.get("session_id")
        if session_id:
            UserSession.objects.filter(id=session_id, user=request.user).update(is_active=False)
        else:
            UserSession.objects.filter(user=request.user).exclude(id=request.session.get("session_id")).update(is_active=False)
        return success_response(message="Sessions terminated successfully.")
