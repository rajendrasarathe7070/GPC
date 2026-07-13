"""Portal admin configuration."""

from django.contrib import admin

from apps.portal.models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "is_published", "show_in_menu", "menu_order", "updated_at"]
    list_filter = ["is_published", "show_in_menu"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
