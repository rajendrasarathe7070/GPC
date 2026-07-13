"""Notices admin configuration."""

from django.contrib import admin

from apps.notices.models import Notice, NoticeCategory, NoticeReadReceipt


@admin.register(NoticeCategory)
class NoticeCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "color", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "priority", "is_pinned", "publish_date", "expiry_date", "view_count", "is_active"]
    list_filter = ["priority", "is_pinned", "is_active", "category", "publish_date"]
    search_fields = ["title", "content", "summary"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish_date"
    raw_id_fields = ["author"]


@admin.register(NoticeReadReceipt)
class NoticeReadReceiptAdmin(admin.ModelAdmin):
    list_display = ["notice", "user", "read_at"]
    list_filter = ["read_at"]
    search_fields = ["notice__title", "user__email"]
