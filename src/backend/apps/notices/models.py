"""Notices models."""

import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from shared.constants import NOTICE_ATTACHMENT_PATH, NoticePriority
from shared.utils.helpers import generate_unique_slug
from shared.utils.validators import DocumentValidator


class NoticeCategory(models.Model):
    """Category for notices."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100, db_index=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#0d6efd")
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notices_notice_category"
        ordering = ["name"]
        verbose_name = "Notice Category"
        verbose_name_plural = "Notice Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.name, NoticeCategory)
        super().save(*args, **kwargs)


class Notice(models.Model):
    """College notice/announcement."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, max_length=255, db_index=True)
    content = models.TextField()
    summary = models.TextField(blank=True)
    category = models.ForeignKey(
        NoticeCategory,
        on_delete=models.PROTECT,
        related_name="notices",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="authored_notices",
    )
    priority = models.CharField(
        max_length=10,
        choices=[(p.value, p.name.replace("_", " ").title()) for p in NoticePriority],
        default=NoticePriority.NORMAL.value,
        db_index=True,
    )
    is_pinned = models.BooleanField(default=False, db_index=True)
    publish_date = models.DateTimeField(default=timezone.now, db_index=True)
    expiry_date = models.DateTimeField(blank=True, null=True, db_index=True)
    attachment = models.FileField(
        upload_to=NOTICE_ATTACHMENT_PATH,
        blank=True,
        null=True,
        validators=[DocumentValidator(max_size=10 * 1024 * 1024)],
    )
    view_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notices_notice"
        ordering = ["-is_pinned", "-publish_date"]
        indexes = [
            models.Index(fields=["category", "is_active", "publish_date"]),
            models.Index(fields=["priority", "is_active"]),
            models.Index(fields=["slug", "is_active"]),
            models.Index(fields=["publish_date", "expiry_date"]),
        ]
        verbose_name = "Notice"
        verbose_name_plural = "Notices"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.title, Notice)
        if not self.summary and self.content:
            self.summary = self.content[:200]
        super().save(*args, **kwargs)

    def is_expired(self):
        if self.expiry_date:
            return timezone.now() > self.expiry_date
        return False


class NoticeReadReceipt(models.Model):
    """Track which users have read a notice."""

    id = models.BigAutoField(primary_key=True)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name="read_receipts")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notice_reads")
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notices_notice_read_receipt"
        unique_together = [["notice", "user"]]
        verbose_name = "Notice Read Receipt"
        verbose_name_plural = "Notice Read Receipts"

    def __str__(self):
        return f"{self.user} read {self.notice.title}"
