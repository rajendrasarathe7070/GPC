"""Local development settings with SQLite for quick demo."""

from .base import *  # noqa: F401,F403

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Remove defender for local demo (no Redis)
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != "defender"]  # noqa: F405
MIDDLEWARE = [m for m in MIDDLEWARE if "defender" not in m]  # noqa: F405

LOGGING["loggers"]["django.db.backends"]["level"] = "DEBUG"  # noqa: F405
