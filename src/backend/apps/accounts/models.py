"""
Accounts Models

Implements:
- Custom User with role-based access
- AuditLog for compliance and security
- ActivityLog for user behavior tracking
- LoginAttempt for brute-force protection
- PasswordResetToken for secure password recovery
- UserSession for multi-device session management
"""

import logging
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from shared.constants import (
    AVATAR_UPLOAD_PATH,
    BloodGroup,
    Gender,
    UserRole,
)
from shared.utils.helpers import generate_unique_slug
from shared.utils.validators import ImageValidator

logger = logging.getLogger("gpc")


class UserManager(models.Manager):
    """Custom manager for User model with security helpers."""

    def get_by_natural_key(self, username):
        """Case-insensitive lookup for authentication."""
        return self.get(**{self.model.USERNAME_FIELD + "__iexact": username})

    def active(self):
        return self.filter(is_active=True)

    def by_role(self, role: UserRole):
        return self.filter(role=role.value)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.model.normalize_username(email).lower().strip()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", UserRole.SUPER_ADMIN.value)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for GPC ERP.

    Supports multiple roles, MFA-ready fields, and comprehensive profile data.
    Designed for future extensibility (Face Recognition, QR Attendance, etc.).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True, db_index=True)
    phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )

    # Identity
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, db_index=True, max_length=100)

    # Role & Status
    role = models.CharField(
        max_length=20,
        choices=[(r.value, r.name.replace("_", " ").title()) for r in UserRole],
        default=UserRole.STUDENT.value,
        db_index=True,
    )
    is_active = models.BooleanField(default=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    # Profile
    avatar = models.ImageField(
        upload_to=AVATAR_UPLOAD_PATH,
        blank=True,
        null=True,
        validators=[ImageValidator(max_size=2 * 1024 * 1024)],
    )
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=20,
        choices=[(g.value, g.name.replace("_", " ").title()) for g in Gender],
        blank=True,
    )
    blood_group = models.CharField(
        max_length=5,
        choices=[(bg.value, bg.value) for bg in BloodGroup],
        blank=True,
    )
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)

    # Security
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=255, blank=True)
    last_password_change = models.DateTimeField(default=timezone.now)
    password_change_required = models.BooleanField(default=False)
    login_count = models.PositiveIntegerField(default=0)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        db_table = "accounts_user"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email", "is_active"]),
            models.Index(fields=["role", "is_active"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["created_at"]),
        ]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"{self.first_name}-{self.last_name}"
            self.slug = generate_unique_slug(base, User)
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_locked(self):
        if self.locked_until and self.locked_until > timezone.now():
            return True
        return False

    def record_login(self, ip_address=None):
        """Update login statistics safely."""
        self.login_count += 1
        self.last_login_ip = ip_address
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=["login_count", "last_login_ip", "failed_login_attempts", "locked_until", "last_login"])

    def record_failed_login(self):
        """Increment failed login attempts and lock if threshold reached."""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_until = timezone.now() + timedelta(minutes=30)
            logger.warning(f"Account locked for user {self.id} due to brute force")
        self.save(update_fields=["failed_login_attempts", "locked_until"])

    def has_role(self, role: UserRole) -> bool:
        """Check if user has a specific role."""
        return self.role == role.value

    def get_role_display_name(self):
        return self.get_role_display()


class AuditLog(models.Model):
    """
    Immutable audit trail for compliance (ISO 27001, government standards).
    """

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    action = models.CharField(max_length=20, db_index=True)
    resource = models.CharField(max_length=255, db_index=True)
    method = models.CharField(max_length=10, blank=True)
    status_code = models.PositiveSmallIntegerField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    duration_ms = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "accounts_audit_log"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["action", "timestamp"]),
            models.Index(fields=["resource", "timestamp"]),
            models.Index(fields=["ip_address", "timestamp"]),
        ]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        return f"[{self.timestamp}] {self.action.upper()} {self.resource}"


class ActivityLog(models.Model):
    """
    User activity tracking for behavior analysis and support.
    """

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activity_logs",
    )
    activity_type = models.CharField(max_length=50, db_index=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "accounts_activity_log"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "activity_type", "created_at"]),
        ]
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"

    def __str__(self):
        return f"{self.user} - {self.activity_type}"


class LoginAttempt(models.Model):
    """
    Tracks login attempts for brute-force detection and IP-based blocking.
    """

    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, db_index=True)
    ip_address = models.GenericIPAddressField(db_index=True)
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    failure_reason = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "accounts_login_attempt"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["ip_address", "success", "created_at"]),
            models.Index(fields=["username", "success", "created_at"]),
        ]
        verbose_name = "Login Attempt"
        verbose_name_plural = "Login Attempts"

    def __str__(self):
        return f"{'SUCCESS' if self.success else 'FAIL'} {self.username} from {self.ip_address}"


class PasswordResetToken(models.Model):
    """
    Secure password reset token with expiration.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
    )
    token_hash = models.CharField(max_length=255, db_index=True)
    expires_at = models.DateTimeField(db_index=True)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts_password_reset_token"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["token_hash", "used", "expires_at"]),
        ]
        verbose_name = "Password Reset Token"
        verbose_name_plural = "Password Reset Tokens"

    def __str__(self):
        return f"Token for {self.user.email}"

    @property
    def is_valid(self):
        return not self.used and self.expires_at > timezone.now()


class UserSession(models.Model):
    """
    Active session tracking for multi-device management and security.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    session_key = models.CharField(max_length=255, db_index=True, blank=True)
    device_name = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts_user_session"
        ordering = ["-last_activity"]
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["session_key", "is_active"]),
        ]
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"

    def __str__(self):
        return f"{self.user} on {self.device_name or 'Unknown Device'}"
