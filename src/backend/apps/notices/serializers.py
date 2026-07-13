"""Notices serializers."""

from rest_framework import serializers

from apps.notices.models import Notice, NoticeCategory, NoticeReadReceipt


class NoticeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeCategory
        fields = ["id", "name", "slug", "description", "color", "is_active"]


class NoticeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_color = serializers.CharField(source="category.color", read_only=True)
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Notice
        fields = [
            "id", "title", "slug", "content", "summary", "category", "category_name", "category_color",
            "author", "author_name", "priority", "is_pinned", "publish_date", "expiry_date",
            "attachment", "view_count", "is_active", "is_expired",
            "meta_title", "meta_description", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "slug", "view_count", "created_at", "updated_at"]


class NoticeReadReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeReadReceipt
        fields = ["id", "notice", "user", "read_at"]
        read_only_fields = ["id", "read_at"]
