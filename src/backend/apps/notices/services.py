"""Notices services."""

from apps.notices.repositories import NoticeCategoryRepository, NoticeReadReceiptRepository, NoticeRepository
from shared.services.base import BaseService


class NoticeCategoryService(BaseService):
    repository = NoticeCategoryRepository


class NoticeService(BaseService):
    repository = NoticeRepository


class NoticeReadReceiptService(BaseService):
    repository = NoticeReadReceiptRepository
