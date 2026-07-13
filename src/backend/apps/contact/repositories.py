"""Contact repositories."""

from apps.contact.models import ContactInfo, Enquiry, Feedback
from shared.repositories.base import BaseRepository


class EnquiryRepository(BaseRepository):
    model = Enquiry


class FeedbackRepository(BaseRepository):
    model = Feedback


class ContactInfoRepository(BaseRepository):
    model = ContactInfo
