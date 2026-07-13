"""Base repository implementing Repository Pattern."""

import logging
from typing import Any, Dict, List, Optional, TypeVar

from django.db import models
from django.db.models import QuerySet

from shared.exceptions import NotFoundError

logger = logging.getLogger("gpc")

ModelType = TypeVar("ModelType", bound=models.Model)


class BaseRepository:
    """Abstract base repository for data access abstraction."""

    model: type[ModelType] = None  # type: ignore

    @classmethod
    def get_by_id(cls, pk: Any, select_related: Optional[List[str]] = None, prefetch_related: Optional[List[str]] = None) -> ModelType:
        """Retrieve a single instance by primary key."""
        qs = cls.model.objects.all()
        if select_related:
            qs = qs.select_related(*select_related)
        if prefetch_related:
            qs = qs.prefetch_related(*prefetch_related)
        try:
            return qs.get(pk=pk)
        except cls.model.DoesNotExist as exc:
            logger.warning(f"{cls.model.__name__} with id {pk} not found")
            raise NotFoundError(f"{cls.model.__name__} not found.") from exc

    @classmethod
    def get_all(cls, order_by: Optional[List[str]] = None) -> QuerySet[ModelType]:
        """Retrieve all instances."""
        qs = cls.model.objects.all()
        if order_by:
            qs = qs.order_by(*order_by)
        return qs

    @classmethod
    def filter(cls, **kwargs) -> QuerySet[ModelType]:
        """Filter instances by given criteria."""
        return cls.model.objects.filter(**kwargs)

    @classmethod
    def create(cls, **kwargs) -> ModelType:
        """Create and return a new instance."""
        try:
            instance = cls.model.objects.create(**kwargs)
            logger.info(f"{cls.model.__name__} created with id {instance.pk}")
            return instance
        except Exception as exc:
            logger.exception(f"Failed to create {cls.model.__name__}")
            raise

    @classmethod
    def update(cls, instance: ModelType, **kwargs) -> ModelType:
        """Update an existing instance."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        try:
            instance.save(update_fields=kwargs.keys())
            logger.info(f"{cls.model.__name__} updated with id {instance.pk}")
            return instance
        except Exception as exc:
            logger.exception(f"Failed to update {cls.model.__name__} with id {instance.pk}")
            raise

    @classmethod
    def delete(cls, instance: ModelType) -> None:
        """Delete an instance."""
        pk = instance.pk
        try:
            instance.delete()
            logger.info(f"{cls.model.__name__} deleted with id {pk}")
        except Exception as exc:
            logger.exception(f"Failed to delete {cls.model.__name__} with id {pk}")
            raise

    @classmethod
    def exists(cls, **kwargs) -> bool:
        """Check if an instance matching criteria exists."""
        return cls.model.objects.filter(**kwargs).exists()

    @classmethod
    def count(cls, **kwargs) -> int:
        """Count instances matching criteria."""
        return cls.model.objects.filter(**kwargs).count()
