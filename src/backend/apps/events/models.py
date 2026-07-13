"""Events models."""

import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from shared.constants import EVENT_IMAGE_PATH, EventCategory
from shared.utils.helpers import generate_unique_slug
from shared.utils.validators import ImageValidator


class EventCategoryModel(models.Model):
    """Event category."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100, db_index=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#198754")
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "events_event_category"
        ordering = ["name"]
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.name, EventCategoryModel)
        super().save(*args, **kwargs)


class Event(models.Model):
    """College event."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, max_length=255, db_index=True)
    description = models.TextField()
    short_description = models.TextField(blank=True)
    category = models.ForeignKey(
        EventCategoryModel,
        on_delete=models.PROTECT,
        related_name="events",
    )
    event_type = models.CharField(
        max_length=20,
        choices=[(c.value, c.name.replace("_", " ").title()) for c in EventCategory],
        default=EventCategory.ACADEMIC.value,
    )
    start_datetime = models.DateTimeField(db_index=True)
    end_datetime = models.DateTimeField(db_index=True)
    venue = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255, blank=True)
    organizer_email = models.EmailField(blank=True)
    image = models.ImageField(
        upload_to=EVENT_IMAGE_PATH,
        blank=True,
        null=True,
        validators=[ImageValidator(max_size=5 * 1024 * 1024)],
    )
    registration_required = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField(blank=True, null=True)
    registration_start = models.DateTimeField(blank=True, null=True)
    registration_end = models.DateTimeField(blank=True, null=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "events_event"
        ordering = ["-start_datetime"]
        indexes = [
            models.Index(fields=["category", "is_active", "start_datetime"]),
            models.Index(fields=["event_type", "is_active"]),
            models.Index(fields=["slug", "is_active"]),
            models.Index(fields=["is_featured", "is_active"]),
            models.Index(fields=["start_datetime", "end_datetime"]),
        ]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.title, Event)
        if not self.short_description and self.description:
            self.short_description = self.description[:200]
        super().save(*args, **kwargs)

    def is_upcoming(self):
        return self.start_datetime > timezone.now()

    def is_ongoing(self):
        now = timezone.now()
        return self.start_datetime <= now <= self.end_datetime

    def is_past(self):
        return self.end_datetime < timezone.now()

    def registration_open(self):
        if not self.registration_required:
            return False
        now = timezone.now()
        if self.registration_start and now < self.registration_start:
            return False
        if self.registration_end and now > self.registration_end:
            return False
        return True


class EventRegistration(models.Model):
    """User registration for an event."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_registrations")
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    attendance_marked_at = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "events_event_registration"
        unique_together = [["event", "user"]]
        ordering = ["-registered_at"]
        verbose_name = "Event Registration"
        verbose_name_plural = "Event Registrations"

    def __str__(self):
        return f"{self.user} registered for {self.event.title}"
