"""Faculty API views."""

import logging

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.faculty.models import FacultyProfile, FacultySubject
from apps.faculty.serializers import FacultyProfileSerializer, FacultySubjectSerializer
from shared.utils.pagination import StandardResultsSetPagination
from shared.utils.response import error_response, success_response

logger = logging.getLogger("gpc")


class FacultyListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            faculty = FacultyProfile.objects.filter(is_active=True, status="active")
            department = request.query_params.get("department")
            designation = request.query_params.get("designation")
            if department:
                faculty = faculty.filter(department__slug=department)
            if designation:
                faculty = faculty.filter(designation=designation)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(faculty, request)
            serializer = FacultyProfileSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Faculty list error")
            return error_response(message="Failed to retrieve faculty.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FacultyDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, employee_id):
        try:
            profile = FacultyProfile.objects.get(employee_id=employee_id, is_active=True)
            serializer = FacultyProfileSerializer(profile)
            return success_response(data=serializer.data)
        except FacultyProfile.DoesNotExist:
            return error_response(message="Faculty not found.", code="not_found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            logger.exception("Faculty detail error")
            return error_response(message="Failed to retrieve faculty.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FacultySubjectListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            assignments = FacultySubject.objects.select_related("faculty", "subject", "session")
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(assignments, request)
            serializer = FacultySubjectSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Faculty subject list error")
            return error_response(message="Failed to retrieve assignments.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
