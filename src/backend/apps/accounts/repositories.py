"""Accounts repository layer."""

from apps.accounts.models import (
    ActivityLog,
    AuditLog,
    LoginAttempt,
    PasswordResetToken,
    User,
    UserSession,
)
from shared.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """Repository for User data access."""

    model = User

    @classmethod
    def get_by_email(cls, email):
        try:
            return cls.model.objects.get(email__iexact=email)
        except cls.model.DoesNotExist:
            from shared.exceptions import NotFoundError
            raise NotFoundError("User not found.")

    @classmethod
    def get_by_slug(cls, slug):
        try:
            return cls.model.objects.get(slug=slug)
        except cls.model.DoesNotExist:
            from shared.exceptions import NotFoundError
            raise NotFoundError("User not found.")


class AuditLogRepository(BaseRepository):
    """Repository for AuditLog data access."""

    model = AuditLog


class ActivityLogRepository(BaseRepository):
    """Repository for ActivityLog data access."""

    model = ActivityLog


class LoginAttemptRepository(BaseRepository):
    """Repository for LoginAttempt data access."""

    model = LoginAttempt


class PasswordResetTokenRepository(BaseRepository):
    """Repository for PasswordResetToken data access."""

    model = PasswordResetToken

    @classmethod
    def get_valid_token(cls, token_hash):
        try:
            return cls.model.objects.get(token_hash=token_hash, used=False, expires_at__gt=__import__("django.utils.timezone").now())
        except cls.model.DoesNotExist:
            from shared.exceptions import NotFoundError
            raise NotFoundError("Invalid or expired token.")


class UserSessionRepository(BaseRepository):
    """Repository for UserSession data access."""

    model = UserSession
