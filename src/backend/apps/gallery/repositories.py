"""Gallery repositories."""

from apps.gallery.models import Album, Media
from shared.repositories.base import BaseRepository


class AlbumRepository(BaseRepository):
    model = Album


class MediaRepository(BaseRepository):
    model = Media
