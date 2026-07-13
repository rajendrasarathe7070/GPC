"""Students serializers."""

from rest_framework import serializers

from apps.students.models import Attendance, ExaminationResult, StudentDocument, StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            "id", "user", "user_name", "user_email", "enrollment_number", "roll_number",
            "course", "course_name", "semester", "admission_date", "category", "status",
            "father_name", "mother_name", "guardian_phone", "aadhaar_number",
            "scholarship_status", "fee_waiver", "remarks", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "enrollment_number", "created_at", "updated_at"]


class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        fields = ["id", "student", "document_type", "file", "verified", "verified_by", "verified_at", "remarks", "uploaded_at"]
        read_only_fields = ["id", "verified", "verified_by", "verified_at", "uploaded_at"]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id", "student", "subject", "date", "status", "marked_by",
            "method", "qr_code_data", "latitude", "longitude", "remarks", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ExaminationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExaminationResult
        fields = [
            "id", "student", "subject", "session", "exam_type",
            "max_marks", "obtained_marks", "grade", "is_pass",
            "remarks", "published", "published_at", "created_at",
        ]
        read_only_fields = ["id", "created_at"]
