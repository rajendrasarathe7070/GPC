"""Contact URL configuration."""

from django.urls import path

from apps.contact.views import (
    ContactInfoListView,
    EnquiryCreateView,
    FeedbackCreateView,
    FeedbackListView,
)

urlpatterns = [
    path("enquiries/", EnquiryCreateView.as_view(), name="enquiry-create"),
    path("feedback/", FeedbackCreateView.as_view(), name="feedback-create"),
    path("feedback/public/", FeedbackListView.as_view(), name="feedback-list"),
    path("info/", ContactInfoListView.as_view(), name="contact-info-list"),
]
