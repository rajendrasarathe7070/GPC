"""Notices API views."""

import logging

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notices.models import Notice, NoticeCategory, NoticeReadReceipt
from apps.notices.serializers import NoticeCategorySerializer, NoticeSerializer
from shared.utils.pagination import StandardResultsSetPagination
from shared.utils.response import error_response, success_response

logger = logging.getLogger("gpc")


class NoticeCategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            categories = NoticeCategory.objects.filter(is_active=True)
            serializer = NoticeCategorySerializer(categories, many=True)
            return success_response(data=serializer.data)
        except Exception as exc:
            logger.exception("Notice category list error")
            return error_response(message="Failed to retrieve categories.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NoticeListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            notices = Notice.objects.filter(
                is_active=True,
                publish_date__lte=timezone.now(),
            ).select_related("category", "author")
            category = request.query_params.get("category")
            priority = request.query_params.get("priority")
            search = request.query_params.get("search")
            if category:
                notices = notices.filter(category__slug=category)
            if priority:
                notices = notices.filter(priority=priority)
            if search:
                notices = notices.filter(title__icontains=search)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(notices, request)
            serializer = NoticeSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Notice list error")
            return error_response(message="Failed to retrieve notices.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NoticeDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            notice = Notice.objects.get(slug=slug, is_active=True)
            notice.view_count += 1
            notice.save(update_fields=["view_count"])
            if request.user.is_authenticated:
                NoticeReadReceipt.objects.get_or_create(notice=notice, user=request.user)
            serializer = NoticeSerializer(notice)
            return success_response(data=serializer.data)
        except Notice.DoesNotExist:
            return error_response(message="Notice not found.", code="not_found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            logger.exception("Notice detail error")
            return error_response(message="Failed to retrieve notice.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
