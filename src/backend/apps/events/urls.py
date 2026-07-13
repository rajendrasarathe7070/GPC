"""Events URL configuration."""

from django.urls import path

from apps.events.views import (
    EventCategoryListView,
    EventDetailView,
    EventListView,
    EventRegisterView,
    MyEventRegistrationsView,
)

urlpatterns = [
    path("categories/", EventCategoryListView.as_view(), name="event-category-list"),
    path("", EventListView.as_view(), name="event-list"),
    path("<slug:slug>/", EventDetailView.as_view(), name="event-detail"),
    path("<uuid:event_id>/register/", EventRegisterView.as_view(), name="event-register"),
    path("my-registrations/", MyEventRegistrationsView.as_view(), name="my-event-registrations"),
]
