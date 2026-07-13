"""Gallery serializers."""

from rest_framework import serializers

from apps.gallery.models import Album, Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["id", "album", "file", "caption", "media_type", "uploaded_by", "is_featured", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class AlbumSerializer(serializers.ModelSerializer):
    media_count = serializers.IntegerField(source="media_items.count", read_only=True)

    class Meta:
        model = Album
        fields = [
            "id", "title", "slug", "description", "cover_image",
            "event_date", "is_featured", "is_active", "media_count", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


class AlbumDetailSerializer(AlbumSerializer):
    media = MediaSerializer(source="media_items", many=True, read_only=True)

    class Meta(AlbumSerializer.Meta):
        fields = AlbumSerializer.Meta.fields + ["media"]
