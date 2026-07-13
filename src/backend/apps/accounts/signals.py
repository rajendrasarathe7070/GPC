"""Signal handlers for accounts app."""

import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.accounts.models import ActivityLog, User

logger = logging.getLogger("gpc")


@receiver(post_save, sender=User)
def log_user_created(sender, instance, created, **kwargs):
    """Log user creation activity."""
    if created:
        try:
            ActivityLog.objects.create(
                user=instance,
                activity_type="account_created",
                description=f"Account created for {instance.email}",
            )
        except Exception as exc:
            logger.error(f"Failed to log account creation: {exc}")


@receiver(post_delete, sender=User)
def log_user_deleted(sender, instance, **kwargs):
    """Log user deletion for audit trail."""
    logger.info(f"User deleted: {instance.email} (ID: {instance.id})")
