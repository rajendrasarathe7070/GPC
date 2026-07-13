"""Gallery URL configuration."""

from django.urls import path

from apps.gallery.views import AlbumDetailView, AlbumListView, MediaListView

urlpatterns = [
    path("albums/", AlbumListView.as_view(), name="album-list"),
    path("albums/<slug:slug>/", AlbumDetailView.as_view(), name="album-detail"),
    path("media/", MediaListView.as_view(), name="media-list"),
]
