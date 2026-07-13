"""Custom validators for GPC ERP."""

import logging
import os

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

logger = logging.getLogger("gpc")

# Optional python-magic with fallback
try:
    import magic
    _magic_available = True
except ImportError:
    _magic_available = False
    magic = None  # type: ignore


@deconstructible
class FileValidator:
    """Validate uploaded files for type and size."""

    def __init__(self, allowed_types=None, max_size=None):
        self.allowed_types = allowed_types or []
        self.max_size = max_size

    def __call__(self, file):
        if self.max_size and file.size > self.max_size:
            raise ValidationError(
                f"File size exceeds maximum allowed size of {self.max_size / (1024 * 1024):.1f} MB."
            )

        if self.allowed_types:
            if _magic_available and magic:
                file.seek(0)
                mime = magic.from_buffer(file.read(2048), mime=True)
                file.seek(0)
            else:
                # Fallback using extension-based detection
                import mimetypes
                mime, _ = mimetypes.guess_type(file.name)
                if not mime:
                    mime = "application/octet-stream"

            if mime not in self.allowed_types:
                logger.warning(f"Rejected file upload with MIME type: {mime}")
                raise ValidationError(f"File type '{mime}' is not allowed.")

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.allowed_types == other.allowed_types and self.max_size == other.max_size


@deconstructible
class ImageValidator(FileValidator):
    """Validate image uploads."""

    def __init__(self, max_size=5 * 1024 * 1024):
        from django.conf import settings
        super().__init__(allowed_types=getattr(settings, "ALLOWED_IMAGE_TYPES", ["image/jpeg", "image/png", "image/webp"]), max_size=max_size)


@deconstructible
class DocumentValidator(FileValidator):
    """Validate document uploads."""

    def __init__(self, max_size=10 * 1024 * 1024):
        from django.conf import settings
        super().__init__(allowed_types=getattr(settings, "ALLOWED_DOCUMENT_TYPES", ["application/pdf"]), max_size=max_size)
