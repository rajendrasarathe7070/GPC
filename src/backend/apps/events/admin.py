"""Events admin configuration."""

from django.contrib import admin

from apps.events.models import Event, EventCategoryModel, EventRegistration


@admin.register(EventCategoryModel)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "color", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "event_type", "start_datetime", "end_datetime", "venue", "registration_required", "is_featured", "is_active"]
    list_filter = ["event_type", "is_featured", "is_active", "registration_required", "start_datetime"]
    search_fields = ["title", "description", "venue", "organizer"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "start_datetime"


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ["event", "user", "registered_at", "attended", "attendance_marked_at"]
    list_filter = ["attended", "registered_at"]
    search_fields = ["event__title", "user__email"]
    raw_id_fields = ["event", "user"]
