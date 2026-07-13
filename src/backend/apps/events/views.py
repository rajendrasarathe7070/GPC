"""Events API views."""

import logging

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.events.models import Event, EventCategoryModel, EventRegistration
from apps.events.serializers import EventCategorySerializer, EventRegistrationSerializer, EventSerializer
from shared.exceptions import GPCException
from shared.utils.pagination import StandardResultsSetPagination
from shared.utils.response import error_response, success_response

logger = logging.getLogger("gpc")


class EventCategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            categories = EventCategoryModel.objects.filter(is_active=True)
            serializer = EventCategorySerializer(categories, many=True)
            return success_response(data=serializer.data)
        except Exception as exc:
            logger.exception("Event category list error")
            return error_response(message="Failed to retrieve categories.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            events = Event.objects.filter(is_active=True)
            event_type = request.query_params.get("type")
            category = request.query_params.get("category")
            status_filter = request.query_params.get("status")
            if event_type:
                events = events.filter(event_type=event_type)
            if category:
                events = events.filter(category__slug=category)
            if status_filter == "upcoming":
                events = events.filter(start_datetime__gt=timezone.now())
            elif status_filter == "ongoing":
                now = timezone.now()
                events = events.filter(start_datetime__lte=now, end_datetime__gte=now)
            elif status_filter == "past":
                events = events.filter(end_datetime__lt=timezone.now())
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(events, request)
            serializer = EventSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Event list error")
            return error_response(message="Failed to retrieve events.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            event = Event.objects.get(slug=slug, is_active=True)
            serializer = EventSerializer(event)
            return success_response(data=serializer.data)
        except Event.DoesNotExist:
            return error_response(message="Event not found.", code="not_found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            logger.exception("Event detail error")
            return error_response(message="Failed to retrieve event.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id, is_active=True)
            if not event.registration_required:
                return error_response(message="Registration not required for this event.", status_code=status.HTTP_400_BAD_REQUEST)
            if not event.registration_open():
                return error_response(message="Registration is closed.", status_code=status.HTTP_400_BAD_REQUEST)
            if event.max_participants and event.registrations.count() >= event.max_participants:
                return error_response(message="Event is full.", status_code=status.HTTP_400_BAD_REQUEST)
            registration, created = EventRegistration.objects.get_or_create(event=event, user=request.user)
            if not created:
                return error_response(message="You are already registered for this event.", status_code=status.HTTP_409_CONFLICT)
            return success_response(data=EventRegistrationSerializer(registration).data, message="Registration successful.", status_code=status.HTTP_201_CREATED)
        except Event.DoesNotExist:
            return error_response(message="Event not found.", code="not_found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            logger.exception("Event registration error")
            return error_response(message="Registration failed.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyEventRegistrationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            registrations = EventRegistration.objects.filter(user=request.user)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(registrations, request)
            serializer = EventRegistrationSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("My registrations error")
            return error_response(message="Failed to retrieve registrations.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
