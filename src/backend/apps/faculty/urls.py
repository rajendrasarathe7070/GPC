"""Faculty URL configuration."""

from django.urls import path

from apps.faculty.views import FacultyDetailView, FacultyListView, FacultySubjectListView

urlpatterns = [
    path("", FacultyListView.as_view(), name="faculty-list"),
    path("<str:employee_id>/", FacultyDetailView.as_view(), name="faculty-detail"),
    path("subjects/", FacultySubjectListView.as_view(), name="faculty-subject-list"),
]
