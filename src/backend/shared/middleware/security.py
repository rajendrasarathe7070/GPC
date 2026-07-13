"""Security middleware for GPC ERP."""

import logging

from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("gpc")


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to every response."""

    def process_response(self, request, response):
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = getattr(settings, "X_FRAME_OPTIONS", "DENY")
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=(), gyroscope=()"
        )
        response["Strict-Transport-Security"] = (
            f"max-age={settings.SECURE_HSTS_SECONDS}; includeSubDomains; preload"
            if settings.SECURE_HSTS_SECONDS
            else ""
        )
        return response


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Apply Content Security Policy headers."""

    def process_response(self, request, response):
        csp_parts = []
        directives = {
            "default-src": getattr(settings, "CSP_DEFAULT_SRC", ("'self'",)),
            "script-src": getattr(settings, "CSP_SCRIPT_SRC", ("'self'",)),
            "style-src": getattr(settings, "CSP_STYLE_SRC", ("'self'",)),
            "font-src": getattr(settings, "CSP_FONT_SRC", ("'self'",)),
            "img-src": getattr(settings, "CSP_IMG_SRC", ("'self'",)),
            "connect-src": getattr(settings, "CSP_CONNECT_SRC", ("'self'",)),
            "frame-ancestors": getattr(settings, "CSP_FRAME_ANCESTORS", ("'none'",)),
        }
        for directive, values in directives.items():
            if values:
                csp_parts.append(f"{directive} {' '.join(values)}")
        if csp_parts:
            response["Content-Security-Policy"] = "; ".join(csp_parts)
        return response
