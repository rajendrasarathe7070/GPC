"""Academics models."""

import uuid

from django.db import models

from shared.utils.helpers import generate_unique_slug


class Department(models.Model):
    """College department."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, db_index=True)
    slug = models.SlugField(unique=True, max_length=100, db_index=True)
    description = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    established_year = models.PositiveSmallIntegerField(blank=True, null=True)
    hod = models.ForeignKey(
        "faculty.FacultyProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="headed_departments",
    )
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    image = models.ImageField(upload_to="departments/%Y/%m/", blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "academics_department"
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.name, Department)
        super().save(*args, **kwargs)


class Course(models.Model):
    """Academic course/program."""

    DURATION_CHOICES = [
        (1, "1 Year"),
        (2, "2 Years"),
        (3, "3 Years"),
        (4, "4 Years"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True, db_index=True)
    slug = models.SlugField(unique=True, max_length=150, db_index=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    duration_years = models.PositiveSmallIntegerField(choices=DURATION_CHOICES, default=3)
    total_semesters = models.PositiveSmallIntegerField(default=6)
    intake_capacity = models.PositiveSmallIntegerField(default=60)
    eligibility = models.TextField(blank=True)
    description = models.TextField(blank=True)
    syllabus_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "academics_course"
        ordering = ["name"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.name, Course)
        super().save(*args, **kwargs)


class Subject(models.Model):
    """Subject within a course."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subjects")
    semester = models.PositiveSmallIntegerField(default=1, db_index=True)
    credits = models.DecimalField(max_digits=3, decimal_places=1, default=3.0)
    theory_hours = models.PositiveSmallIntegerField(default=3)
    practical_hours = models.PositiveSmallIntegerField(default=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "academics_subject"
        ordering = ["course", "semester", "name"]
        unique_together = [["course", "code"]]
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"{self.name} ({self.code})"


class AcademicSession(models.Model):
    """Academic year session."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)  # e.g., 2024-2025
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "academics_academic_session"
        ordering = ["-start_date"]
        verbose_name = "Academic Session"
        verbose_name_plural = "Academic Sessions"

    def __str__(self):
        return self.name


class Semester(models.Model):
    """Running semester instance."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="semesters")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="semesters")
    semester_number = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "academics_semester"
        ordering = ["-start_date"]
        unique_together = [["session", "course", "semester_number"]]
        verbose_name = "Semester"
        verbose_name_plural = "Semesters"

    def __str__(self):
        return f"{self.course.name} - Semester {self.semester_number} ({self.session.name})"
