"""Gallery services."""

from apps.gallery.repositories import AlbumRepository, MediaRepository
from shared.services.base import BaseService


class AlbumService(BaseService):
    repository = AlbumRepository


class MediaService(BaseService):
    repository = MediaRepository
