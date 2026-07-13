"""Faculty models."""

import uuid

from django.conf import settings
from django.db import models

from shared.constants import FACULTY_DOCUMENT_PATH
from shared.utils.validators import DocumentValidator, ImageValidator


class FacultyProfile(models.Model):
    """Faculty profile linked to User."""

    DESIGNATION_CHOICES = [
        ("principal", "Principal"),
        ("vice_principal", "Vice Principal"),
        ("hod", "Head of Department"),
        ("professor", "Professor"),
        ("associate_professor", "Associate Professor"),
        ("assistant_professor", "Assistant Professor"),
        ("lecturer", "Lecturer"),
        ("lab_assistant", "Lab Assistant"),
        ("visiting_faculty", "Visiting Faculty"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("on_leave", "On Leave"),
        ("retired", "Retired"),
        ("resigned", "Resigned"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="faculty_profile",
    )
    employee_id = models.CharField(max_length=20, unique=True, db_index=True)
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.PROTECT,
        related_name="faculty_members",
    )
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES, default="lecturer")
    joining_date = models.DateField()
    qualification = models.CharField(max_length=255, blank=True)
    specialization = models.CharField(max_length=255, blank=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    publications = models.TextField(blank=True)
    research_area = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", db_index=True)
    bio = models.TextField(blank=True)
    office_room = models.CharField(max_length=50, blank=True)
    office_hours = models.CharField(max_length=100, blank=True)
    resume = models.FileField(upload_to=FACULTY_DOCUMENT_PATH, blank=True, null=True, validators=[DocumentValidator()])
    profile_image = models.ImageField(upload_to="faculty/images/%Y/%m/", blank=True, null=True, validators=[ImageValidator(max_size=2 * 1024 * 1024)])
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "faculty_faculty_profile"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["employee_id", "status"]),
            models.Index(fields=["department", "status"]),
            models.Index(fields=["designation", "status"]),
        ]
        verbose_name = "Faculty Profile"
        verbose_name_plural = "Faculty Profiles"

    def __str__(self):
        return f"{self.employee_id} - {self.user.full_name}"


class FacultySubject(models.Model):
    """Mapping faculty to subjects per session."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name="assigned_subjects")
    subject = models.ForeignKey("academics.Subject", on_delete=models.CASCADE, related_name="faculty_assignments")
    session = models.ForeignKey("academics.AcademicSession", on_delete=models.CASCADE, related_name="faculty_subjects")
    is_primary = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "faculty_faculty_subject"
        unique_together = [["faculty", "subject", "session"]]
        verbose_name = "Faculty Subject Assignment"
        verbose_name_plural = "Faculty Subject Assignments"

    def __str__(self):
        return f"{self.faculty.user.full_name} -> {self.subject.name} ({self.session.name})"
