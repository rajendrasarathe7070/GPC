"""Template context processors."""

from django.conf import settings


def site_context(request):
    """Add site-wide context variables to every template."""
    return {
        "SITE_URL": getattr(settings, "SITE_URL", ""),
        "SITE_NAME": getattr(settings, "SITE_NAME", ""),
        "DEBUG": getattr(settings, "DEBUG", False),
        "CURRENT_YEAR": __import__("datetime").datetime.now().year,
    }
