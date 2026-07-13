"""Gallery API views."""

import logging

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.gallery.models import Album, Media
from apps.gallery.serializers import AlbumDetailSerializer, AlbumSerializer, MediaSerializer
from shared.utils.pagination import StandardResultsSetPagination
from shared.utils.response import error_response, success_response

logger = logging.getLogger("gpc")


class AlbumListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            albums = Album.objects.filter(is_active=True)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(albums, request)
            serializer = AlbumSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Album list error")
            return error_response(message="Failed to retrieve albums.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlbumDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            album = Album.objects.get(slug=slug, is_active=True)
            serializer = AlbumDetailSerializer(album)
            return success_response(data=serializer.data)
        except Album.DoesNotExist:
            return error_response(message="Album not found.", code="not_found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            logger.exception("Album detail error")
            return error_response(message="Failed to retrieve album.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MediaListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            media = Media.objects.filter(album__is_active=True)
            album = request.query_params.get("album")
            if album:
                media = media.filter(album__slug=album)
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(media, request)
            serializer = MediaSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as exc:
            logger.exception("Media list error")
            return error_response(message="Failed to retrieve media.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
