"""Faculty repositories."""

from apps.faculty.models import FacultyProfile, FacultySubject
from shared.repositories.base import BaseRepository


class FacultyProfileRepository(BaseRepository):
    model = FacultyProfile


class FacultySubjectRepository(BaseRepository):
    model = FacultySubject
