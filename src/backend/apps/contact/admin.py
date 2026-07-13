"""Contact admin configuration."""

from django.contrib import admin

from apps.contact.models import ContactInfo, Enquiry, Feedback


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "status", "assigned_to", "created_at", "resolved_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["name", "email", "subject", "message"]
    raw_id_fields = ["assigned_to"]
    date_hierarchy = "created_at"


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "rating", "is_public", "created_at"]
    list_filter = ["rating", "is_public", "created_at"]
    search_fields = ["name", "email", "comment"]


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ["title", "department", "email", "phone", "is_primary", "is_active"]
    list_filter = ["is_primary", "is_active"]
    search_fields = ["title", "email", "phone"]
