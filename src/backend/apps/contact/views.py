"""Contact API views."""

import logging

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.contact.models import ContactInfo, Enquiry, Feedback
from apps.contact.serializers import ContactInfoSerializer, EnquirySerializer, FeedbackSerializer
from shared.utils.pagination import StandardResultsSetPagination
from shared.utils.response import error_response, success_response

logger = logging.getLogger("gpc")


class EnquiryCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EnquirySerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message="Validation failed.", code="validation_error", errors=serializer.errors)
        try:
            serializer.save()
            return success_response(data=serializer.data, message="Enquiry submitted successfully.", status_code=status.HTTP_201_CREATED)
        except Exception as exc:
            logger.exception("Enquiry creation error")
            return error_response(message="Failed to submit enquiry.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FeedbackCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message="Validation failed.", code="validation_error", errors=serializer.errors)
        try:
            serializer.save()
            return success_response(data=serializer.data, message="Feedback submitted successfully.", status_code=status.HTTP_201_CREATED)
        except Exception as exc:
            logger.exception("Feedback creation error")
            return error_response(message="Failed to submit feedback.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FeedbackListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            feedbacks = Feedback.objects.filter(is_public=True)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(feedbacks, request)
            serializer = FeedbackSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Feedback list error")
            return error_response(message="Failed to retrieve feedback.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContactInfoListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            infos = ContactInfo.objects.filter(is_active=True)
            serializer = ContactInfoSerializer(infos, many=True)
            return success_response(data=serializer.data)
        except Exception as exc:
            logger.exception("Contact info list error")
            return error_response(message="Failed to retrieve contact info.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
