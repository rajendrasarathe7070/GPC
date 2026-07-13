"""Contact services."""

from apps.contact.repositories import ContactInfoRepository, EnquiryRepository, FeedbackRepository
from shared.services.base import BaseService


class EnquiryService(BaseService):
    repository = EnquiryRepository


class FeedbackService(BaseService):
    repository = FeedbackRepository


class ContactInfoService(BaseService):
    repository = ContactInfoRepository
