"""Academics repositories."""

from apps.academics.models import AcademicSession, Course, Department, Semester, Subject
from shared.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository):
    model = Department


class CourseRepository(BaseRepository):
    model = Course


class SubjectRepository(BaseRepository):
    model = Subject


class AcademicSessionRepository(BaseRepository):
    model = AcademicSession


class SemesterRepository(BaseRepository):
    model = Semester
