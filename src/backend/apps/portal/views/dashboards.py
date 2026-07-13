"""Dashboard views for authenticated users."""

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

logger = logging.getLogger("gpc")


@login_required
def student_dashboard(request):
    """Student dashboard view."""
    context = {
        "page_title": "Student Dashboard",
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Dashboard", "url": None},
        ],
    }
    return render(request, "pages/portal/student/dashboard.html", context)


@login_required
def faculty_dashboard(request):
    """Faculty dashboard view."""
    context = {
        "page_title": "Faculty Dashboard",
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Dashboard", "url": None},
        ],
    }
    return render(request, "pages/portal/faculty/dashboard.html", context)


@login_required
def admin_dashboard(request):
    """Admin dashboard view (redirects to Django admin or custom)."""
    context = {
        "page_title": "Admin Dashboard",
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Admin Dashboard", "url": None},
        ],
    }
    return render(request, "pages/portal/admin/dashboard.html", context)
