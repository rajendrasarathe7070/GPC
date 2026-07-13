"""General helper utilities."""

import logging
import re
import uuid
from datetime import datetime

from django.utils.text import slugify

logger = logging.getLogger("gpc")


def generate_unique_slug(base_text, model_class, field_name="slug"):
    """Generate a unique slug for a model instance."""
    base_slug = slugify(base_text)[:50]
    unique_slug = base_slug
    counter = 1
    while model_class.objects.filter(**{field_name: unique_slug}).exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1
    return unique_slug


def generate_enrollment_number(course_code, year):
    """Generate a unique enrollment number."""
    timestamp = datetime.now().strftime("%y%m%d")
    random_suffix = uuid.uuid4().hex[:4].upper()
    return f"{course_code}{year}{timestamp}{random_suffix}"


def sanitize_filename(filename):
    """Sanitize a filename to prevent path traversal and unsafe chars."""
    filename = re.sub(r"[^\w\s.-]", "", filename).strip()
    filename = re.sub(r"\s+", "_", filename)
    return filename


def format_phone_number(phone):
    """Format and validate Indian phone number."""
    phone = re.sub(r"\D", "", phone)
    if len(phone) == 10:
        return f"+91{phone}"
    if len(phone) == 12 and phone.startswith("91"):
        return f"+{phone}"
    if len(phone) == 13 and phone.startswith("+91"):
        return phone
    return None


def log_exception(logger_instance, exc, context=None):
    """Log an exception with structured context."""
    extra = {"context": context or {}}
    logger_instance.exception(str(exc), extra=extra)
