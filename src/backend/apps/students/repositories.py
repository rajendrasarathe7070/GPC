"""Students repositories."""

from apps.students.models import Attendance, ExaminationResult, StudentDocument, StudentProfile
from shared.repositories.base import BaseRepository


class StudentProfileRepository(BaseRepository):
    model = StudentProfile


class StudentDocumentRepository(BaseRepository):
    model = StudentDocument


class AttendanceRepository(BaseRepository):
    model = Attendance


class ExaminationResultRepository(BaseRepository):
    model = ExaminationResult
