"""Gallery models."""

import uuid

from django.conf import settings
from django.db import models

from shared.constants import GALLERY_PATH, MediaType
from shared.utils.helpers import generate_unique_slug
from shared.utils.validators import DocumentValidator, ImageValidator


class Album(models.Model):
    """Photo/video album."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=150, db_index=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(
        upload_to="gallery/album_covers/%Y/%m/",
        blank=True,
        null=True,
        validators=[ImageValidator(max_size=2 * 1024 * 1024)],
    )
    event_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "gallery_album"
        ordering = ["-event_date", "-created_at"]
        verbose_name = "Album"
        verbose_name_plural = "Albums"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.title, Album)
        super().save(*args, **kwargs)


class Media(models.Model):
    """Individual media item."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="media_items",
    )
    file = models.FileField(
        upload_to=GALLERY_PATH,
        validators=[ImageValidator(max_size=5 * 1024 * 1024)],
    )
    caption = models.CharField(max_length=255, blank=True)
    media_type = models.CharField(
        max_length=10,
        choices=[(m.value, m.name.title()) for m in MediaType],
        default=MediaType.IMAGE.value,
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_media",
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "gallery_media"
        ordering = ["-uploaded_at"]
        verbose_name = "Media"
        verbose_name_plural = "Media"

    def __str__(self):
        return f"{self.album.title} - {self.caption or self.id}"
