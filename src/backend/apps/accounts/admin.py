"""Accounts admin configuration."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import (
    ActivityLog,
    AuditLog,
    LoginAttempt,
    PasswordResetToken,
    User,
    UserSession,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with security fields."""

    list_display = [
        "email", "full_name", "role", "is_active", "is_staff",
        "is_email_verified", "last_login", "created_at",
    ]
    list_filter = ["role", "is_active", "is_staff", "is_email_verified", "gender", "created_at"]
    search_fields = ["email", "first_name", "last_name", "phone", "slug"]
    ordering = ["-created_at"]
    readonly_fields = ["id", "slug", "login_count", "last_login_ip", "failed_login_attempts", "created_at", "updated_at"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone", "avatar", "date_of_birth", "gender", "blood_group")}),
        (_("Address"), {"fields": ("address", "city", "state", "pincode")}),
        (_("Emergency Contact"), {"fields": ("emergency_contact_name", "emergency_contact_phone")}),
        (_("Role & Status"), {"fields": ("role", "is_active", "is_staff", "is_superuser", "is_email_verified", "is_phone_verified")}),
        (_("Security"), {"fields": ("mfa_enabled", "last_password_change", "password_change_required", "login_count", "last_login_ip", "failed_login_attempts", "locked_until")}),
        (_("Permissions"), {"fields": ("groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "role", "password1", "password2"),
        }),
    )

    @admin.display(description="Full Name")
    def full_name(self, obj):
        return obj.full_name


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "action", "resource", "user", "ip_address", "status_code", "duration_ms"]
    list_filter = ["action", "status_code", "timestamp"]
    search_fields = ["resource", "user__email", "ip_address"]
    readonly_fields = ["id", "timestamp"]
    date_hierarchy = "timestamp"


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ["created_at", "user", "activity_type", "ip_address"]
    list_filter = ["activity_type", "created_at"]
    search_fields = ["user__email", "description"]
    readonly_fields = ["id", "created_at"]


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ["created_at", "username", "ip_address", "success", "failure_reason"]
    list_filter = ["success", "failure_reason", "created_at"]
    search_fields = ["username", "ip_address"]
    readonly_fields = ["id", "created_at"]


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "used", "expires_at", "created_at"]
    list_filter = ["used", "created_at"]
    search_fields = ["user__email"]
    readonly_fields = ["id", "token_hash", "created_at"]


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ["user", "device_name", "ip_address", "is_active", "last_activity", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["user__email", "device_name", "ip_address"]
    readonly_fields = ["id", "created_at"]
