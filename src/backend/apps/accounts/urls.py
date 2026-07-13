"""Accounts URL configuration."""

from django.urls import path

from apps.accounts.views import (
    ActivityLogListView,
    AuditLogListView,
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    ProfileView,
    RegisterView,
    SessionListView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("profile/", ProfileView.as_view(), name="auth-profile"),
    path("change-password/", PasswordChangeView.as_view(), name="auth-change-password"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="auth-password-reset"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="auth-password-reset-confirm"),
    path("audit-logs/", AuditLogListView.as_view(), name="auth-audit-logs"),
    path("activity-logs/", ActivityLogListView.as_view(), name="auth-activity-logs"),
    path("sessions/", SessionListView.as_view(), name="auth-sessions"),
]
