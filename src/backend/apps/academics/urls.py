"""Academics URL configuration."""

from django.urls import path

from apps.academics.views import (
    AcademicSessionListView,
    CourseDetailView,
    CourseListView,
    DepartmentDetailView,
    DepartmentListView,
    SemesterListView,
    SubjectListView,
)

urlpatterns = [
    path("departments/", DepartmentListView.as_view(), name="department-list"),
    path("departments/<slug:slug>/", DepartmentDetailView.as_view(), name="department-detail"),
    path("courses/", CourseListView.as_view(), name="course-list"),
    path("courses/<slug:slug>/", CourseDetailView.as_view(), name="course-detail"),
    path("subjects/", SubjectListView.as_view(), name="subject-list"),
    path("sessions/", AcademicSessionListView.as_view(), name="session-list"),
    path("semesters/", SemesterListView.as_view(), name="semester-list"),
]
