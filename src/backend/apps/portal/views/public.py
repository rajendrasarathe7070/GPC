"""Public portal views (SEO-optimized, server-rendered)."""

import logging

from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from apps.academics.models import Course, Department
from apps.events.models import Event
from apps.gallery.models import Album
from apps.notices.models import Notice
from apps.portal.models import Page

logger = logging.getLogger("gpc")


def _seo_context(title, description, canonical, og_image=None):
    return {
        "page_title": title,
        "meta_description": description,
        "canonical_url": canonical,
        "og_title": title,
        "og_description": description,
        "og_image": og_image or "/static/images/og-default.jpg",
        "twitter_card": "summary_large_image",
    }


@require_GET
def home_view(request):
    """Homepage with featured content."""
    context = {
        "notices": Notice.objects.filter(is_active=True)[:5],
        "events": Event.objects.filter(is_active=True, is_featured=True)[:4],
        "departments": Department.objects.filter(is_active=True)[:6],
        "albums": Album.objects.filter(is_active=True, is_featured=True)[:4],
        ** _seo_context(
            title="Government Polytechnic College - Official Website",
            description="Welcome to Government Polytechnic College. Explore courses, admissions, notices, and events.",
            canonical=request.build_absolute_uri("/"),
        ),
        "breadcrumb": [{"label": "Home", "url": "/"}],
    }
    return render(request, "pages/public/home.html", context)


@require_GET
def about_view(request):
    """About page."""
    page = get_object_or_404(Page, slug="about", is_published=True)
    context = {
        "page": page,
        ** _seo_context(
            title=f"About Us - {page.title}",
            description=page.meta_description or "Learn about Government Polytechnic College, our history, mission, and vision.",
            canonical=request.build_absolute_uri("/about/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "About Us", "url": None},
        ],
    }
    return render(request, "pages/public/page.html", context)


@require_GET
def department_list_view(request):
    """Department listing page."""
    departments = Department.objects.filter(is_active=True).annotate(course_count=Count("courses"))
    context = {
        "departments": departments,
        ** _seo_context(
            title="Departments - Government Polytechnic College",
            description="Explore our academic departments, faculty, and programs.",
            canonical=request.build_absolute_uri("/departments/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Departments", "url": None},
        ],
    }
    return render(request, "pages/public/departments.html", context)


@require_GET
def department_detail_view(request, slug):
    """Department detail page."""
    department = get_object_or_404(Department, slug=slug, is_active=True)
    context = {
        "department": department,
        "courses": department.courses.filter(is_active=True),
        "faculty": department.faculty_members.filter(is_active=True, status="active"),
        ** _seo_context(
            title=f"{department.name} Department - Government Polytechnic College",
            description=department.meta_description or f"Learn about the {department.name} department, courses, and faculty.",
            canonical=request.build_absolute_uri(f"/departments/{slug}/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Departments", "url": "/departments/"},
            {"label": department.name, "url": None},
        ],
    }
    return render(request, "pages/public/department_detail.html", context)


@require_GET
def course_list_view(request):
    """Course listing page."""
    courses = Course.objects.filter(is_active=True).select_related("department")
    context = {
        "courses": courses,
        ** _seo_context(
            title="Courses & Programs - Government Polytechnic College",
            description="Browse diploma and certificate courses offered at our college.",
            canonical=request.build_absolute_uri("/courses/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Courses", "url": None},
        ],
    }
    return render(request, "pages/public/courses.html", context)


@require_GET
def course_detail_view(request, slug):
    """Course detail page."""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    context = {
        "course": course,
        "subjects": course.subjects.filter(is_active=True),
        ** _seo_context(
            title=f"{course.name} - Government Polytechnic College",
            description=course.meta_description or f"Learn about the {course.name} program, eligibility, syllabus, and intake.",
            canonical=request.build_absolute_uri(f"/courses/{slug}/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Courses", "url": "/courses/"},
            {"label": course.name, "url": None},
        ],
    }
    return render(request, "pages/public/course_detail.html", context)


@require_GET
def faculty_list_view(request):
    """Faculty listing page."""
    from apps.faculty.models import FacultyProfile
    faculty = FacultyProfile.objects.filter(is_active=True, status="active").select_related("user", "department")
    context = {
        "faculty": faculty,
        ** _seo_context(
            title="Faculty - Government Polytechnic College",
            description="Meet our experienced faculty members across all departments.",
            canonical=request.build_absolute_uri("/faculty/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Faculty", "url": None},
        ],
    }
    return render(request, "pages/public/faculty.html", context)


@require_GET
def notice_list_view(request):
    """Notice listing page."""
    from django.utils import timezone
    notices = Notice.objects.filter(is_active=True, publish_date__lte=timezone.now()).select_related("category")
    context = {
        "notices": notices,
        ** _seo_context(
            title="Notices & Announcements - Government Polytechnic College",
            description="Latest notices, circulars, and announcements from the college.",
            canonical=request.build_absolute_uri("/notices/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Notices", "url": None},
        ],
    }
    return render(request, "pages/public/notices.html", context)


@require_GET
def notice_detail_view(request, slug):
    """Notice detail page."""
    notice = get_object_or_404(Notice, slug=slug, is_active=True)
    context = {
        "notice": notice,
        ** _seo_context(
            title=f"{notice.title} - Government Polytechnic College",
            description=notice.meta_description or notice.summary,
            canonical=request.build_absolute_uri(f"/notices/{slug}/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Notices", "url": "/notices/"},
            {"label": notice.title, "url": None},
        ],
    }
    return render(request, "pages/public/notice_detail.html", context)


@require_GET
def event_list_view(request):
    """Event listing page."""
    from django.utils import timezone
    events = Event.objects.filter(is_active=True).select_related("category")
    context = {
        "events": events,
        ** _seo_context(
            title="Events - Government Polytechnic College",
            description="Upcoming and past events, workshops, seminars, and cultural programs.",
            canonical=request.build_absolute_uri("/events/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Events", "url": None},
        ],
    }
    return render(request, "pages/public/events.html", context)


@require_GET
def event_detail_view(request, slug):
    """Event detail page."""
    event = get_object_or_404(Event, slug=slug, is_active=True)
    context = {
        "event": event,
        ** _seo_context(
            title=f"{event.title} - Government Polytechnic College",
            description=event.meta_description or event.short_description,
            canonical=request.build_absolute_uri(f"/events/{slug}/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Events", "url": "/events/"},
            {"label": event.title, "url": None},
        ],
    }
    return render(request, "pages/public/event_detail.html", context)


@require_GET
def gallery_list_view(request):
    """Gallery listing page."""
    albums = Album.objects.filter(is_active=True)
    context = {
        "albums": albums,
        ** _seo_context(
            title="Gallery - Government Polytechnic College",
            description="Photo and video gallery of college events, infrastructure, and activities.",
            canonical=request.build_absolute_uri("/gallery/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Gallery", "url": None},
        ],
    }
    return render(request, "pages/public/gallery.html", context)


@require_GET
def gallery_detail_view(request, slug):
    """Gallery album detail page."""
    album = get_object_or_404(Album, slug=slug, is_active=True)
    context = {
        "album": album,
        "media": album.media_items.all(),
        ** _seo_context(
            title=f"{album.title} - Gallery - Government Polytechnic College",
            description=album.description or "View photos and videos from this album.",
            canonical=request.build_absolute_uri(f"/gallery/{slug}/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Gallery", "url": "/gallery/"},
            {"label": album.title, "url": None},
        ],
    }
    return render(request, "pages/public/gallery_detail.html", context)


@require_GET
def contact_view(request):
    """Contact page."""
    from apps.contact.models import ContactInfo
    contact_infos = ContactInfo.objects.filter(is_active=True).select_related("department")
    context = {
        "contact_infos": contact_infos,
        ** _seo_context(
            title="Contact Us - Government Polytechnic College",
            description="Get in touch with us for admissions, enquiries, and general information.",
            canonical=request.build_absolute_uri("/contact/"),
        ),
        "breadcrumb": [
            {"label": "Home", "url": "/"},
            {"label": "Contact Us", "url": None},
        ],
    }
    return render(request, "pages/public/contact.html", context)
