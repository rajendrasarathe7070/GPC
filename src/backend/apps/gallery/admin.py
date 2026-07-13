"""Gallery admin configuration."""

from django.contrib import admin

from apps.gallery.models import Album, Media


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "event_date", "is_featured", "is_active", "created_at"]
    list_filter = ["is_featured", "is_active", "event_date"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ["album", "caption", "media_type", "is_featured", "uploaded_at"]
    list_filter = ["media_type", "is_featured", "uploaded_at"]
    search_fields = ["caption", "album__title"]
