"""Accounts API serializers."""

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.accounts.models import ActivityLog, AuditLog, User, UserSession
from shared.constants import Gender, UserRole


class UserSerializer(serializers.ModelSerializer):
    """Base user serializer."""

    role_display = serializers.CharField(source="get_role_display", read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "full_name", "slug",
            "role", "role_display", "phone", "avatar", "is_active",
            "is_email_verified", "date_of_birth", "gender", "blood_group",
            "address", "city", "state", "pincode",
            "emergency_contact_name", "emergency_contact_phone",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "slug", "is_active", "is_email_verified", "created_at", "updated_at"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email", "password", "password_confirm",
            "first_name", "last_name", "role", "phone",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        from apps.accounts.services import AuthService
        return AuthService.register(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError({"new_password_confirm": "Passwords do not match."})
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for password reset request."""

    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation."""

    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError({"new_password_confirm": "Passwords do not match."})
        return attrs


class TokenResponseSerializer(serializers.Serializer):
    """Serializer for token response."""

    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for audit logs."""

    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id", "user_email", "action", "resource", "method",
            "status_code", "ip_address", "duration_ms", "metadata", "timestamp",
        ]
        read_only_fields = fields


class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for activity logs."""

    class Meta:
        model = ActivityLog
        fields = ["id", "activity_type", "description", "ip_address", "created_at"]
        read_only_fields = fields


class UserSessionSerializer(serializers.ModelSerializer):
    """Serializer for user sessions."""

    class Meta:
        model = UserSession
        fields = [
            "id", "device_name", "ip_address", "location",
            "is_active", "last_activity", "created_at",
        ]
        read_only_fields = fields
