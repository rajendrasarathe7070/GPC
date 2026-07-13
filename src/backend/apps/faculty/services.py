"""Faculty services."""

from apps.faculty.repositories import FacultyProfileRepository, FacultySubjectRepository
from shared.services.base import BaseService


class FacultyProfileService(BaseService):
    repository = FacultyProfileRepository


class FacultySubjectService(BaseService):
    repository = FacultySubjectRepository
