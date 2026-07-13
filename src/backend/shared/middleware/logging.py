"""Request logging middleware."""

import logging
import time

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("gpc")


class RequestLoggingMiddleware(MiddlewareMixin):
    """Log all incoming requests with timing and metadata."""

    def process_request(self, request):
        request._request_start_time = time.time()

    def process_response(self, request, response):
        if not hasattr(request, "_request_start_time"):
            return response

        duration = round((time.time() - request._request_start_time) * 1000, 2)
        user_id = request.user.id if hasattr(request, "user") and request.user.is_authenticated else None

        logger.info(
            "Request processed",
            extra={
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "duration_ms": duration,
                "user_id": user_id,
                "ip": self._get_client_ip(request),
            },
        )
        return response

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")
