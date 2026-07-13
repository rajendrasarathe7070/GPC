"""Accounts business logic services."""

import hashlib
import logging
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import LoginAttempt, PasswordResetToken, UserSession
from apps.accounts.repositories import (
    LoginAttemptRepository,
    PasswordResetTokenRepository,
    UserRepository,
    UserSessionRepository,
)
from shared.constants import AuditAction
from shared.exceptions import (
    AuthenticationError,
    PermissionDeniedError,
    RateLimitError,
    ValidationError,
)
from shared.services.base import BaseService
from shared.utils.helpers import log_exception

logger = logging.getLogger("gpc")


class AuthService(BaseService):
    """Authentication and authorization business logic."""

    repository = UserRepository

    @classmethod
    def register(cls, email, password, first_name, last_name, role="student", **extra_fields):
        """Register a new user with validation and secure defaults."""
        if UserRepository.exists(email__iexact=email):
            raise ValidationError("A user with this email already exists.", code="email_exists")

        try:
            user = UserRepository.create(
                email=email.lower().strip(),
                first_name=first_name.strip(),
                last_name=last_name.strip(),
                role=role,
                **extra_fields,
            )
            user.set_password(password)
            user.save(update_fields=["password", "last_password_change"])
            return user
        except Exception as exc:
            log_exception(logger, exc, context={"email": email})
            raise ValidationError("Registration failed. Please try again.") from exc

    @classmethod
    def login(cls, request, email, password):
        """Authenticate user and generate JWT tokens with session tracking."""
        ip_address = cls._get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:512]

        # Rate limit check by IP
        recent_attempts = LoginAttemptRepository.filter(
            ip_address=ip_address,
            success=False,
            created_at__gte=timezone.now() - timedelta(minutes=5),
        ).count()
        if recent_attempts >= 10:
            logger.warning(f"Rate limit hit for IP {ip_address}")
            raise RateLimitError("Too many failed attempts. Please try again later.")

        user = authenticate(request, username=email, password=password)

        if user is None:
            LoginAttemptRepository.create(
                username=email,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                failure_reason="invalid_credentials",
            )
            raise AuthenticationError("Invalid email or password.")

        if not user.is_active:
            LoginAttemptRepository.create(
                username=email,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                failure_reason="account_inactive",
            )
            raise PermissionDeniedError("Account is inactive. Contact administration.")

        if user.is_locked:
            LoginAttemptRepository.create(
                username=email,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                failure_reason="account_locked",
            )
            raise PermissionDeniedError("Account is temporarily locked due to multiple failed attempts.")

        # Success
        user.record_login(ip_address=ip_address)
        LoginAttemptRepository.create(
            username=email,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
        )

        # Create session record
        UserSessionRepository.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            device_name=cls._parse_device(user_agent),
        )

        refresh = RefreshToken.for_user(user)
        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @classmethod
    def logout(cls, user, refresh_token_str=None):
        """Blacklist refresh token and deactivate sessions."""
        if refresh_token_str:
            try:
                token = RefreshToken(refresh_token_str)
                token.blacklist()
            except Exception as exc:
                logger.warning(f"Token blacklist failed: {exc}")
        UserSessionRepository.filter(user=user).update(is_active=False)
        return True

    @classmethod
    def change_password(cls, user, old_password, new_password):
        """Secure password change with validation."""
        if not user.check_password(old_password):
            raise ValidationError("Current password is incorrect.", code="wrong_password")
        user.set_password(new_password)
        user.last_password_change = timezone.now()
        user.password_change_required = False
        user.save(update_fields=["password", "last_password_change", "password_change_required"])
        return True

    @classmethod
    def request_password_reset(cls, email):
        """Generate a secure password reset token and send email."""
        try:
            user = UserRepository.get_by_email(email)
        except Exception:
            # Do not reveal whether email exists
            logger.info(f"Password reset requested for non-existent email: {email}")
            return True

        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        PasswordResetTokenRepository.create(
            user=user,
            token_hash=token_hash,
            expires_at=timezone.now() + timedelta(hours=24),
        )

        reset_url = f"{settings.SITE_URL}/auth/reset-password?token={raw_token}"
        subject = "Password Reset Request"
        message = render_to_string("emails/password_reset.txt", {"user": user, "reset_url": reset_url})
        html_message = render_to_string("emails/password_reset.html", {"user": user, "reset_url": reset_url})

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=True,
        )
        return True

    @classmethod
    def reset_password(cls, raw_token, new_password):
        """Reset password using a valid token."""
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        token = PasswordResetTokenRepository.get_valid_token(token_hash)
        user = token.user
        user.set_password(new_password)
        user.last_password_change = timezone.now()
        user.save(update_fields=["password", "last_password_change"])
        token.used = True
        token.save(update_fields=["used"])
        return True

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")

    @staticmethod
    def _parse_device(user_agent):
        ua = user_agent.lower()
        if "mobile" in ua:
            return "Mobile"
        if "tablet" in ua:
            return "Tablet"
        return "Desktop"


class UserService(BaseService):
    """User management business logic."""

    repository = UserRepository

    @classmethod
    def get_profile(cls, user_id):
        return cls.retrieve(user_id)

    @classmethod
    def update_profile(cls, user_id, **kwargs):
        forbidden = {"password", "is_superuser", "is_staff", "role", "is_active"}
        updates = {k: v for k, v in kwargs.items() if k not in forbidden}
        return cls.update(user_id, **updates)


class AuditService:
    """Audit log service."""

    @staticmethod
    def log(user, action, resource, **kwargs):
        from apps.accounts.repositories import AuditLogRepository
        try:
            AuditLogRepository.create(
                user=user,
                action=action,
                resource=resource,
                **kwargs,
            )
        except Exception as exc:
            logger.error(f"Audit log creation failed: {exc}")
