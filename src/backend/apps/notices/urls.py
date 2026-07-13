"""Notices URL configuration."""

from django.urls import path

from apps.notices.views import NoticeCategoryListView, NoticeDetailView, NoticeListView

urlpatterns = [
    path("categories/", NoticeCategoryListView.as_view(), name="notice-category-list"),
    path("", NoticeListView.as_view(), name="notice-list"),
    path("<slug:slug>/", NoticeDetailView.as_view(), name="notice-detail"),
]
