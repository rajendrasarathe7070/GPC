"""Students URL configuration."""

from django.urls import path

from apps.students.views import (
    AttendanceListView,
    ResultListView,
    StudentDocumentListView,
    StudentProfileView,
)

urlpatterns = [
    path("profile/", StudentProfileView.as_view(), name="student-profile"),
    path("documents/", StudentDocumentListView.as_view(), name="student-documents"),
    path("attendance/", AttendanceListView.as_view(), name="student-attendance"),
    path("results/", ResultListView.as_view(), name="student-results"),
]
