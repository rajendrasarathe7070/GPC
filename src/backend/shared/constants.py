"""Shared constants for GPC ERP."""

from enum import Enum


class UserRole(str, Enum):
    """System user roles."""

    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    STAFF = "staff"
    FACULTY = "faculty"
    STUDENT = "student"
    PARENT = "parent"
    LIBRARIAN = "librarian"
    ACCOUNTANT = "accountant"


class Gender(str, Enum):
    """Gender choices."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class BloodGroup(str, Enum):
    """Blood group choices."""

    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class NoticePriority(str, Enum):
    """Notice priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class EventCategory(str, Enum):
    """Event categories."""

    ACADEMIC = "academic"
    CULTURAL = "cultural"
    SPORTS = "sports"
    TECHNICAL = "technical"
    SEMINAR = "seminar"
    WORKSHOP = "workshop"
    OTHER = "other"


class EnquiryStatus(str, Enum):
    """Enquiry resolution status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class MediaType(str, Enum):
    """Gallery media types."""

    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"


class AuditAction(str, Enum):
    """Audit log actions."""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    VIEW = "view"
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    EXPORT = "export"
    IMPORT = "import"


# Pagination defaults
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Cache timeouts (seconds)
CACHE_TIMEOUT_SHORT = 300      # 5 minutes
CACHE_TIMEOUT_MEDIUM = 3600    # 1 hour
CACHE_TIMEOUT_LONG = 86400     # 1 day

# File paths
AVATAR_UPLOAD_PATH = "accounts/avatars/%Y/%m/"
NOTICE_ATTACHMENT_PATH = "notices/attachments/%Y/%m/"
EVENT_IMAGE_PATH = "events/images/%Y/%m/"
GALLERY_PATH = "gallery/%Y/%m/"
STUDENT_DOCUMENT_PATH = "students/documents/%Y/%m/"
FACULTY_DOCUMENT_PATH = "faculty/documents/%Y/%m/"
