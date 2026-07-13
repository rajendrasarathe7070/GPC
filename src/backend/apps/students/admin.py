"""Students admin configuration."""

from django.contrib import admin

from apps.students.models import Attendance, ExaminationResult, StudentDocument, StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["enrollment_number", "user", "course", "roll_number", "status", "admission_date"]
    list_filter = ["status", "category", "course", "admission_date"]
    search_fields = ["enrollment_number", "roll_number", "user__email", "user__first_name", "user__last_name", "aadhaar_number"]
    raw_id_fields = ["user", "course", "semester"]


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ["student", "document_type", "verified", "uploaded_at"]
    list_filter = ["document_type", "verified", "uploaded_at"]
    search_fields = ["student__enrollment_number"]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["student", "subject", "date", "status", "method", "created_at"]
    list_filter = ["status", "method", "date"]
    search_fields = ["student__enrollment_number", "qr_code_data"]
    date_hierarchy = "date"


@admin.register(ExaminationResult)
class ExaminationResultAdmin(admin.ModelAdmin):
    list_display = ["student", "subject", "exam_type", "obtained_marks", "max_marks", "grade", "is_pass", "published"]
    list_filter = ["exam_type", "is_pass", "published", "session"]
    search_fields = ["student__enrollment_number"]
