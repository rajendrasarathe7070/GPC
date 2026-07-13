"""Academics API views."""

import logging

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.academics.models import AcademicSession, Course, Department, Semester, Subject
from apps.academics.serializers import (
    AcademicSessionSerializer,
    CourseSerializer,
    DepartmentSerializer,
    SemesterSerializer,
    SubjectSerializer,
)
from shared.exceptions import GPCException
from shared.utils.pagination import StandardResultsSetPagination
from shared.utils.response import error_response, success_response

logger = logging.getLogger("gpc")


class DepartmentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            departments = Department.objects.filter(is_active=True)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(departments, request)
            serializer = DepartmentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Department list error")
            return error_response(message="Failed to retrieve departments.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartmentDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            department = Department.objects.get(slug=slug, is_active=True)
            serializer = DepartmentSerializer(department)
            return success_response(data=serializer.data)
        except Department.DoesNotExist:
            return error_response(message="Department not found.", code="not_found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            logger.exception("Department detail error")
            return error_response(message="Failed to retrieve department.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CourseListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            courses = Course.objects.filter(is_active=True)
            department = request.query_params.get("department")
            if department:
                courses = courses.filter(department__slug=department)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(courses, request)
            serializer = CourseSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Course list error")
            return error_response(message="Failed to retrieve courses.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CourseDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            course = Course.objects.get(slug=slug, is_active=True)
            serializer = CourseSerializer(course)
            return success_response(data=serializer.data)
        except Course.DoesNotExist:
            return error_response(message="Course not found.", code="not_found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            logger.exception("Course detail error")
            return error_response(message="Failed to retrieve course.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            subjects = Subject.objects.filter(is_active=True)
            course = request.query_params.get("course")
            semester = request.query_params.get("semester")
            if course:
                subjects = subjects.filter(course__slug=course)
            if semester:
                subjects = subjects.filter(semester=semester)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(subjects, request)
            serializer = SubjectSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Subject list error")
            return error_response(message="Failed to retrieve subjects.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AcademicSessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sessions = AcademicSession.objects.all()
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(sessions, request)
            serializer = AcademicSessionSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Academic session list error")
            return error_response(message="Failed to retrieve sessions.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SemesterListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            semesters = Semester.objects.filter(is_active=True)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(semesters, request)
            serializer = SemesterSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Semester list error")
            return error_response(message="Failed to retrieve semesters.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
