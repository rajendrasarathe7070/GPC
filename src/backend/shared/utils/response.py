"""Standardized API response utilities."""

import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from shared.exceptions import GPCException

logger = logging.getLogger("gpc")


def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    """Return a standardized success response."""
    return Response({
        "success": True,
        "message": message,
        "data": data,
    }, status=status_code)


def error_response(message="Error", code="error", status_code=status.HTTP_400_BAD_REQUEST, errors=None):
    """Return a standardized error response."""
    payload = {
        "success": False,
        "message": message,
        "code": code,
    }
    if errors is not None:
        payload["errors"] = errors
    return Response(payload, status=status_code)


def custom_exception_handler(exc, context):
    """Custom DRF exception handler for consistent error formatting."""
    response = exception_handler(exc, context)

    if isinstance(exc, GPCException):
        logger.warning(f"GPCException: {exc.message}", extra={"code": exc.code})
        return error_response(
            message=exc.message,
            code=exc.code,
            status_code=exc.status_code,
        )

    if response is not None:
        message = response.data.get("detail", "Request failed.")
        errors = response.data if "detail" not in response.data else None
        return error_response(
            message=message,
            code="request_error",
            status_code=response.status_code,
            errors=errors,
        )

    logger.exception("Unhandled exception in API", exc_info=exc)
    return error_response(
        message="An unexpected error occurred. Please try again later.",
        code="internal_error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
