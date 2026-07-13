"""Events serializers."""

from rest_framework import serializers

from apps.events.models import Event, EventCategoryModel, EventRegistration


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategoryModel
        fields = ["id", "name", "slug", "description", "color", "is_active"]


class EventSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_color = serializers.CharField(source="category.color", read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    registration_open = serializers.BooleanField(read_only=True)
    registered_count = serializers.IntegerField(source="registrations.count", read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "title", "slug", "description", "short_description",
            "category", "category_name", "category_color", "event_type",
            "start_datetime", "end_datetime", "venue", "organizer", "organizer_email",
            "image", "registration_required", "max_participants", "registration_start",
            "registration_end", "is_featured", "is_active",
            "is_upcoming", "is_ongoing", "is_past", "registration_open", "registered_count",
            "meta_title", "meta_description", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


class EventRegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source="event.title", read_only=True)
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = EventRegistration
        fields = ["id", "event", "event_title", "user", "user_name", "registered_at", "attended", "attendance_marked_at", "remarks"]
        read_only_fields = ["id", "registered_at", "attendance_marked_at"]
