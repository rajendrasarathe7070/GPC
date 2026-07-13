"""Events repositories."""

from apps.events.models import Event, EventCategoryModel, EventRegistration
from shared.repositories.base import BaseRepository


class EventCategoryRepository(BaseRepository):
    model = EventCategoryModel


class EventRepository(BaseRepository):
    model = Event


class EventRegistrationRepository(BaseRepository):
    model = EventRegistration
