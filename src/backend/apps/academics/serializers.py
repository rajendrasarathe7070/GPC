"""Academics serializers."""

from rest_framework import serializers

from apps.academics.models import AcademicSession, Course, Department, Semester, Subject


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id", "name", "code", "slug", "description", "vision", "mission",
            "established_year", "email", "phone", "image", "is_active",
            "meta_title", "meta_description", "created_at", "updated_at",
        ]


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "name", "code", "slug", "department", "department_name",
            "duration_years", "total_semesters", "intake_capacity",
            "eligibility", "description", "syllabus_url", "is_active",
            "meta_title", "meta_description", "created_at", "updated_at",
        ]


class SubjectSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Subject
        fields = [
            "id", "name", "code", "course", "course_name", "semester",
            "credits", "theory_hours", "practical_hours", "description", "is_active",
            "created_at", "updated_at",
        ]


class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ["id", "name", "start_date", "end_date", "is_active", "created_at"]


class SemesterSerializer(serializers.ModelSerializer):
    session_name = serializers.CharField(source="session.name", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Semester
        fields = [
            "id", "session", "session_name", "course", "course_name",
            "semester_number", "start_date", "end_date", "is_active", "created_at",
        ]
