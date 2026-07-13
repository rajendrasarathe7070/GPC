"""Students API views."""

import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.students.models import Attendance, ExaminationResult, StudentDocument, StudentProfile
from apps.students.serializers import (
    AttendanceSerializer,
    ExaminationResultSerializer,
    StudentDocumentSerializer,
    StudentProfileSerializer,
)
from shared.exceptions import GPCException
from shared.utils.pagination import StandardResultsSetPagination
from shared.utils.response import error_response, success_response

logger = logging.getLogger("gpc")


class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = StudentProfile.objects.get(user=request.user)
            serializer = StudentProfileSerializer(profile)
            return success_response(data=serializer.data)
        except StudentProfile.DoesNotExist:
            return error_response(message="Student profile not found.", code="not_found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            logger.exception("Student profile error")
            return error_response(message="Failed to retrieve profile.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentDocumentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = StudentProfile.objects.get(user=request.user)
            docs = StudentDocument.objects.filter(student=profile)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(docs, request)
            serializer = StudentDocumentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Student documents error")
            return error_response(message="Failed to retrieve documents.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AttendanceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = StudentProfile.objects.get(user=request.user)
            attendances = Attendance.objects.filter(student=profile)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(attendances, request)
            serializer = AttendanceSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Attendance list error")
            return error_response(message="Failed to retrieve attendance.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResultListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = StudentProfile.objects.get(user=request.user)
            results = ExaminationResult.objects.filter(student=profile, published=True)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(results, request)
            serializer = ExaminationResultSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Result list error")
            return error_response(message="Failed to retrieve results.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
