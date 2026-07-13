"""Custom exceptions for GPC ERP."""


class GPCException(Exception):
    """Base exception for GPC ERP."""

    def __init__(self, message="An error occurred.", code="error", status_code=500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(GPCException):
    """Raised when input validation fails."""

    def __init__(self, message="Validation failed.", code="validation_error"):
        super().__init__(message=message, code=code, status_code=400)


class AuthenticationError(GPCException):
    """Raised on authentication failures."""

    def __init__(self, message="Authentication failed.", code="authentication_error"):
        super().__init__(message=message, code=code, status_code=401)


class PermissionDeniedError(GPCException):
    """Raised when user lacks permission."""

    def __init__(self, message="Permission denied.", code="permission_denied"):
        super().__init__(message=message, code=code, status_code=403)


class NotFoundError(GPCException):
    """Raised when a resource is not found."""

    def __init__(self, message="Resource not found.", code="not_found"):
        super().__init__(message=message, code=code, status_code=404)


class ConflictError(GPCException):
    """Raised on resource conflict."""

    def __init__(self, message="Resource conflict.", code="conflict"):
        super().__init__(message=message, code=code, status_code=409)


class RateLimitError(GPCException):
    """Raised when rate limit is exceeded."""

    def __init__(self, message="Rate limit exceeded.", code="rate_limit_exceeded"):
        super().__init__(message=message, code=code, status_code=429)


class ServiceUnavailableError(GPCException):
    """Raised when an external service is unavailable."""

    def __init__(self, message="Service temporarily unavailable.", code="service_unavailable"):
        super().__init__(message=message, code=code, status_code=503)
