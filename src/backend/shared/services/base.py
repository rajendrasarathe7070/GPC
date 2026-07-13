"""Base service implementing business logic abstraction."""

import logging
from typing import Any, Dict, List, Optional

from django.db import transaction

from shared.exceptions import GPCException, ValidationError

logger = logging.getLogger("gpc")


class BaseService:
    """Abstract base service for business logic encapsulation."""

    repository = None

    @classmethod
    def list(cls, filters: Optional[Dict[str, Any]] = None, order_by: Optional[List[str]] = None):
        """List resources with optional filtering and ordering."""
        try:
            qs = cls.repository.get_all(order_by=order_by)
            if filters:
                qs = qs.filter(**filters)
            return qs
        except Exception as exc:
            logger.exception("Failed to list resources")
            raise GPCException("Unable to retrieve resources.") from exc

    @classmethod
    def retrieve(cls, pk: Any):
        """Retrieve a single resource by primary key."""
        try:
            return cls.repository.get_by_id(pk)
        except GPCException:
            raise
        except Exception as exc:
            logger.exception(f"Failed to retrieve resource with id {pk}")
            raise GPCException("Unable to retrieve resource.") from exc

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs):
        """Create a new resource within a transaction."""
        try:
            return cls.repository.create(**kwargs)
        except ValidationError:
            raise
        except Exception as exc:
            logger.exception("Failed to create resource")
            raise GPCException("Unable to create resource.") from exc

    @classmethod
    @transaction.atomic
    def update(cls, pk: Any, **kwargs):
        """Update an existing resource within a transaction."""
        try:
            instance = cls.repository.get_by_id(pk)
            return cls.repository.update(instance, **kwargs)
        except GPCException:
            raise
        except Exception as exc:
            logger.exception(f"Failed to update resource with id {pk}")
            raise GPCException("Unable to update resource.") from exc

    @classmethod
    @transaction.atomic
    def delete(cls, pk: Any):
        """Delete a resource within a transaction."""
        try:
            instance = cls.repository.get_by_id(pk)
            cls.repository.delete(instance)
        except GPCException:
            raise
        except Exception as exc:
            logger.exception(f"Failed to delete resource with id {pk}")
            raise GPCException("Unable to delete resource.") from exc
