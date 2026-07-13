"""Contact models."""

import uuid

from django.conf import settings
from django.db import models

from shared.constants import EnquiryStatus


class Enquiry(models.Model):
    """Public enquiry/complaint."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[(s.value, s.name.replace("_", " ").title()) for s in EnquiryStatus],
        default=EnquiryStatus.PENDING.value,
        db_index=True,
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_enquiries",
    )
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "contact_enquiry"
        ordering = ["-created_at"]
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Feedback(models.Model):
    """Public feedback."""

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    is_public = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contact_feedback"
        ordering = ["-created_at"]
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"{self.name} - {self.rating}/5"


class ContactInfo(models.Model):
    """Department-wise contact information."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.CASCADE,
        related_name="contact_infos",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    alternate_phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    map_url = models.URLField(blank=True)
    office_hours = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contact_contact_info"
        ordering = ["-is_primary", "title"]
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Infos"

    def __str__(self):
        return self.title
