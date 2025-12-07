# repositories/repository_factory.py
from repositories.user_repository import UserRepository
from repositories.course_repository import CourseRepository
from repositories.lecture_repository import LectureRepository
from repositories.assignment_repository import AssignmentRepository
from repositories.submission_repository import SubmissionRepository
from repositories.attendance_repository import AttendanceRepository

class RepositoryFactory:
    @staticmethod
    def get(name: str):
        name = name.lower()
        if name == "user":
            return UserRepository()
        if name == "course":
            return CourseRepository()
        if name == "lecture":
            return LectureRepository()
        if name == "assignment":
            return AssignmentRepository()
        if name == "submission":
            return SubmissionRepository()
        if name == "attendance":
            return AttendanceRepository()
        raise ValueError(f"Unknown repository: {name}")
