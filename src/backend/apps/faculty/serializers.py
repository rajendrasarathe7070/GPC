"""Faculty serializers."""

from rest_framework import serializers

from apps.faculty.models import FacultyProfile, FacultySubject


class FacultyProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = FacultyProfile
        fields = [
            "id", "user", "user_name", "user_email", "employee_id", "department", "department_name",
            "designation", "joining_date", "qualification", "specialization", "experience_years",
            "publications", "research_area", "status", "bio", "office_room", "office_hours",
            "resume", "profile_image", "is_active", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "employee_id", "created_at", "updated_at"]


class FacultySubjectSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source="faculty.user.full_name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    session_name = serializers.CharField(source="session.name", read_only=True)

    class Meta:
        model = FacultySubject
        fields = ["id", "faculty", "faculty_name", "subject", "subject_name", "session", "session_name", "is_primary", "created_at"]
        read_only_fields = ["id", "created_at"]
