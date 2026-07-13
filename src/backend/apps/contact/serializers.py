"""Contact serializers."""

from rest_framework import serializers

from apps.contact.models import ContactInfo, Enquiry, Feedback


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = [
            "id", "name", "email", "phone", "subject", "message",
            "status", "assigned_to", "resolution_notes", "created_at", "resolved_at",
        ]
        read_only_fields = ["id", "status", "assigned_to", "resolution_notes", "created_at", "resolved_at"]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "name", "email", "rating", "comment", "is_public", "created_at"]
        read_only_fields = ["id", "is_public", "created_at"]


class ContactInfoSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = ContactInfo
        fields = [
            "id", "department", "department_name", "title", "email",
            "phone", "alternate_phone", "address", "map_url", "office_hours",
            "is_primary", "is_active", "created_at",
        ]
        read_only_fields = ["id", "created_at"]
