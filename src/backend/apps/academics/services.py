"""Academics services."""

from apps.academics.repositories import (
    AcademicSessionRepository,
    CourseRepository,
    DepartmentRepository,
    SemesterRepository,
    SubjectRepository,
)
from shared.services.base import BaseService


class DepartmentService(BaseService):
    repository = DepartmentRepository


class CourseService(BaseService):
    repository = CourseRepository


class SubjectService(BaseService):
    repository = SubjectRepository


class AcademicSessionService(BaseService):
    repository = AcademicSessionRepository


class SemesterService(BaseService):
    repository = SemesterRepository
