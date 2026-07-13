"""Academics admin configuration."""

from django.contrib import admin

from apps.academics.models import AcademicSession, Course, Department, Semester, Subject


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "hod", "established_year", "is_active"]
    list_filter = ["is_active", "established_year"]
    search_fields = ["name", "code", "description"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "department", "duration_years", "intake_capacity", "is_active"]
    list_filter = ["is_active", "duration_years", "department"]
    search_fields = ["name", "code"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "course", "semester", "credits", "is_active"]
    list_filter = ["is_active", "semester", "course"]
    search_fields = ["name", "code"]


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ["session", "course", "semester_number", "start_date", "end_date", "is_active"]
    list_filter = ["is_active", "semester_number"]
    search_fields = ["course__name", "session__name"]
