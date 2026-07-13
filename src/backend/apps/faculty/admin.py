"""Faculty admin configuration."""

from django.contrib import admin

from apps.faculty.models import FacultyProfile, FacultySubject


@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ["employee_id", "user", "department", "designation", "joining_date", "status", "is_active"]
    list_filter = ["status", "designation", "department", "is_active"]
    search_fields = ["employee_id", "user__email", "user__first_name", "user__last_name"]
    raw_id_fields = ["user", "department"]


@admin.register(FacultySubject)
class FacultySubjectAdmin(admin.ModelAdmin):
    list_display = ["faculty", "subject", "session", "is_primary", "created_at"]
    list_filter = ["is_primary", "session"]
    search_fields = ["faculty__user__email", "subject__name"]
    raw_id_fields = ["faculty", "subject", "session"]
