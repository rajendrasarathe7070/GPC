"""Audit logging middleware."""

import json
import logging
import time

from django.utils.deprecation import MiddlewareMixin

from apps.accounts.models import AuditLog
from shared.constants import AuditAction

logger = logging.getLogger("audit")


class AuditLogMiddleware(MiddlewareMixin):
    """Log significant request events for audit trails."""

    def process_request(self, request):
        request._audit_start_time = time.time()

    def process_response(self, request, response):
        if not hasattr(request, "_audit_start_time"):
            return response

        duration = round((time.time() - request._audit_start_time) * 1000, 2)
        user = request.user if hasattr(request, "user") and request.user.is_authenticated else None
        path = request.path
        method = request.method
        status_code = response.status_code

        # Determine action
        action = AuditAction.VIEW
        if method == "POST":
            action = AuditAction.CREATE
        elif method == "PUT" or method == "PATCH":
            action = AuditAction.UPDATE
        elif method == "DELETE":
            action = AuditAction.DELETE

        # Skip static/media/admin assets
        if path.startswith(("/static/", "/media/", "/__debug__/")):
            return response

        try:
            AuditLog.objects.create(
                user=user,
                action=action.value,
                resource=path,
                method=method,
                status_code=status_code,
                ip_address=self._get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:512],
                duration_ms=duration,
                metadata={
                    "query_params": dict(request.GET),
                },
            )
        except Exception as exc:
            logger.error(f"Failed to write audit log: {exc}")

        return response

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")
