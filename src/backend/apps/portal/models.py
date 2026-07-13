"""Portal models."""

import uuid

from django.db import models

from shared.utils.helpers import generate_unique_slug


class Page(models.Model):
    """Dynamic CMS page for static content (About, Mission, Vision, etc.)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, db_index=True)
    content = models.TextField()
    template = models.CharField(max_length=50, default="pages/public/page.html")
    is_published = models.BooleanField(default=True, db_index=True)
    show_in_menu = models.BooleanField(default=False)
    menu_order = models.PositiveSmallIntegerField(default=0)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "portal_page"
        ordering = ["menu_order", "title"]
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.title, Page)
        super().save(*args, **kwargs)
