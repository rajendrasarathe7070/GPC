"""Custom error views."""

import logging

from django.shortcuts import render

logger = logging.getLogger("gpc")


def bad_request_view(request, exception=None):
    logger.warning(f"400 Bad Request: {request.path}")
    return render(request, "errors/400.html", status=400)


def permission_denied_view(request, exception=None):
    logger.warning(f"403 Permission Denied: {request.path} - User: {request.user}")
    return render(request, "errors/403.html", status=403)


def page_not_found_view(request, exception=None):
    logger.warning(f"404 Not Found: {request.path}")
    return render(request, "errors/404.html", status=404)


def server_error_view(request):
    logger.error(f"500 Server Error: {request.path}")
    return render(request, "errors/500.html", status=500)
