"""Portal URL configuration."""

from django.urls import path

from apps.portal.views.dashboards import admin_dashboard, faculty_dashboard, student_dashboard
from apps.portal.views.public import (
    about_view,
    contact_view,
    course_detail_view,
    course_list_view,
    department_detail_view,
    department_list_view,
    event_detail_view,
    event_list_view,
    faculty_list_view,
    gallery_detail_view,
    gallery_list_view,
    home_view,
    notice_detail_view,
    notice_list_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("departments/", department_list_view, name="department-list-page"),
    path("departments/<slug:slug>/", department_detail_view, name="department-detail-page"),
    path("courses/", course_list_view, name="course-list-page"),
    path("courses/<slug:slug>/", course_detail_view, name="course-detail-page"),
    path("faculty/", faculty_list_view, name="faculty-list-page"),
    path("notices/", notice_list_view, name="notice-list-page"),
    path("notices/<slug:slug>/", notice_detail_view, name="notice-detail-page"),
    path("events/", event_list_view, name="event-list-page"),
    path("events/<slug:slug>/", event_detail_view, name="event-detail-page"),
    path("gallery/", gallery_list_view, name="gallery-list-page"),
    path("gallery/<slug:slug>/", gallery_detail_view, name="gallery-detail-page"),
    path("contact/", contact_view, name="contact-page"),
    path("portal/student/", student_dashboard, name="student-dashboard"),
    path("portal/faculty/", faculty_dashboard, name="faculty-dashboard"),
    path("portal/admin/", admin_dashboard, name="admin-dashboard"),
]
