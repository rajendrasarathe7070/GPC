"""Sitemap configurations for SEO."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.academics.models import Department
from apps.events.models import Event
from apps.notices.models import Notice


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["home", "about", "department-list-page", "course-list-page", "faculty-list-page", "notice-list-page", "event-list-page", "gallery-list-page", "contact-page"]

    def location(self, item):
        return reverse(item)


class NoticeSitemap(Sitemap):
    """Sitemap for notices."""

    priority = 0.6
    changefreq = "daily"

    def items(self):
        return Notice.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("notice-detail-page", kwargs={"slug": obj.slug})


class EventSitemap(Sitemap):
    """Sitemap for events."""

    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Event.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("event-detail-page", kwargs={"slug": obj.slug})


class DepartmentSitemap(Sitemap):
    """Sitemap for departments."""

    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return Department.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("department-detail-page", kwargs={"slug": obj.slug})
