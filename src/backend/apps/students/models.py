"""Students models."""

import uuid

from django.conf import settings
from django.db import models

from shared.constants import STUDENT_DOCUMENT_PATH
from shared.utils.validators import DocumentValidator, ImageValidator


class StudentProfile(models.Model):
    """Student profile linked to User."""

    CATEGORY_CHOICES = [
        ("general", "General"),
        ("obc", "OBC"),
        ("sc", "SC"),
        ("st", "ST"),
        ("ews", "EWS"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("passed_out", "Passed Out"),
        ("transferred", "Transferred"),
        ("suspended", "Suspended"),
        ("expelled", "Expelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    enrollment_number = models.CharField(max_length=30, unique=True, db_index=True)
    roll_number = models.CharField(max_length=20, db_index=True)
    course = models.ForeignKey(
        "academics.Course",
        on_delete=models.PROTECT,
        related_name="students",
    )
    semester = models.ForeignKey(
        "academics.Semester",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    admission_date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="general")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", db_index=True)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    aadhaar_number = models.CharField(max_length=12, blank=True, db_index=True)
    scholarship_status = models.BooleanField(default=False)
    fee_waiver = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "students_student_profile"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["enrollment_number", "status"]),
            models.Index(fields=["course", "status"]),
            models.Index(fields=["roll_number"]),
        ]
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"

    def __str__(self):
        return f"{self.enrollment_number} - {self.user.full_name}"


class StudentDocument(models.Model):
    """Documents uploaded by or for students."""

    DOCUMENT_TYPE_CHOICES = [
        ("photo", "Passport Photo"),
        ("signature", "Signature"),
        ("tenth_marksheet", "10th Marksheet"),
        ("twelfth_marksheet", "12th Marksheet"),
        ("domicile", "Domicile Certificate"),
        ("caste_certificate", "Caste Certificate"),
        ("income_certificate", "Income Certificate"),
        ("transfer_certificate", "Transfer Certificate"),
        ("character_certificate", "Character Certificate"),
        ("medical_certificate", "Medical Certificate"),
        ("other", "Other"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(
        upload_to=STUDENT_DOCUMENT_PATH,
        validators=[DocumentValidator(max_size=10 * 1024 * 1024)],
    )
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_documents",
    )
    verified_at = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "students_student_document"
        ordering = ["-uploaded_at"]
        verbose_name = "Student Document"
        verbose_name_plural = "Student Documents"

    def __str__(self):
        return f"{self.student.enrollment_number} - {self.get_document_type_display()}"


class Attendance(models.Model):
    """Future-ready attendance model (QR / Face recognition ready)."""

    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("excused", "Excused"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendances")
    subject = models.ForeignKey("academics.Subject", on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="present")
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="marked_attendances",
    )
    method = models.CharField(
        max_length=20,
        choices=[("manual", "Manual"), ("qr", "QR Scan"), ("face", "Face Recognition"), ("biometric", "Biometric")],
        default="manual",
    )
    qr_code_data = models.CharField(max_length=255, blank=True, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "students_attendance"
        ordering = ["-date", "-created_at"]
        unique_together = [["student", "subject", "date"]]
        indexes = [
            models.Index(fields=["student", "date"]),
            models.Index(fields=["subject", "date"]),
            models.Index(fields=["qr_code_data"]),
        ]
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance Records"

    def __str__(self):
        return f"{self.student.enrollment_number} - {self.date} - {self.status}"


class ExaminationResult(models.Model):
    """Future-ready examination result model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="results")
    subject = models.ForeignKey("academics.Subject", on_delete=models.CASCADE, related_name="results")
    session = models.ForeignKey("academics.AcademicSession", on_delete=models.CASCADE, related_name="results")
    exam_type = models.CharField(
        max_length=20,
        choices=[("internal", "Internal"), ("external", "External"), ("practical", "Practical"), ("viva", "Viva")],
    )
    max_marks = models.DecimalField(max_digits=6, decimal_places=2)
    obtained_marks = models.DecimalField(max_digits=6, decimal_places=2)
    grade = models.CharField(max_length=5, blank=True)
    is_pass = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    published = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "students_examination_result"
        ordering = ["-created_at"]
        verbose_name = "Examination Result"
        verbose_name_plural = "Examination Results"

    def __str__(self):
        return f"{self.student.enrollment_number} - {self.subject.code} - {self.obtained_marks}/{self.max_marks}"
