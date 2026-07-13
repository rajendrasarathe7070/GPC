"""Events services."""

from apps.events.repositories import EventCategoryRepository, EventRegistrationRepository, EventRepository
from shared.services.base import BaseService


class EventCategoryService(BaseService):
    repository = EventCategoryRepository


class EventService(BaseService):
    repository = EventRepository


class EventRegistrationService(BaseService):
    repository = EventRegistrationRepository
