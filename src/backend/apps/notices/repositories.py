"""Notices repositories."""

from apps.notices.models import Notice, NoticeCategory, NoticeReadReceipt
from shared.repositories.base import BaseRepository


class NoticeCategoryRepository(BaseRepository):
    model = NoticeCategory


class NoticeRepository(BaseRepository):
    model = Notice


class NoticeReadReceiptRepository(BaseRepository):
    model = NoticeReadReceipt
