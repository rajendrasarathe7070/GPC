"""
GPC ERP URL Configuration

Public Pages: SEO-optimized, server-rendered
API Endpoints: RESTful JSON for portals and future mobile apps
Admin: Django built-in admin with customizations
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.portal.sitemaps import (
    DepartmentSitemap,
    EventSitemap,
    NoticeSitemap,
    StaticViewSitemap,
)

sitemaps = {
    "static": StaticViewSitemap,
    "notices": NoticeSitemap,
    "events": EventSitemap,
    "departments": DepartmentSitemap,
}

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),


    # Public Portal (SEO-optimized pages)
    path("", include("apps.portal.urls")),

    # API v1
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/academics/", include("apps.academics.urls")),
    path("api/v1/students/", include("apps.students.urls")),
    path("api/v1/faculty/", include("apps.faculty.urls")),
    path("api/v1/notices/", include("apps.notices.urls")),
    path("api/v1/events/", include("apps.events.urls")),
    path("api/v1/gallery/", include("apps.gallery.urls")),
    path("api/v1/contact/", include("apps.contact.urls")),

    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # SEO
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", include("apps.portal.robots_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

# Custom error handlers
handler400 = "apps.portal.views.errors.bad_request_view"
handler403 = "apps.portal.views.errors.permission_denied_view"
handler404 = "apps.portal.views.errors.page_not_found_view"
handler500 = "apps.portal.views.errors.server_error_view"
