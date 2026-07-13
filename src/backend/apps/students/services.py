"""Students services."""

from apps.students.repositories import (
    AttendanceRepository,
    ExaminationResultRepository,
    StudentDocumentRepository,
    StudentProfileRepository,
)
from shared.services.base import BaseService


class StudentProfileService(BaseService):
    repository = StudentProfileRepository


class StudentDocumentService(BaseService):
    repository = StudentDocumentRepository


class AttendanceService(BaseService):
    repository = AttendanceRepository


class ExaminationResultService(BaseService):
    repository = ExaminationResultRepository
