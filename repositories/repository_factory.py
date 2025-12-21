# repositories/repository_factory.py
from repositories.user_repository import UserRepository
from repositories.course_repository import CourseRepository
from repositories.lecture_repository import LectureRepository
from repositories.assignment_repository import AssignmentRepository
from repositories.submission_repository import SubmissionRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.chat_repository import ChatRepository
from repositories.enrollment_repository import EnrollmentRepository
from repositories.announcement_repository import AnnouncementRepository
from repositories.notification_repository import NotificationRepository


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
        if name == "chat":
            return ChatRepository()
        if name == "enrollment":
            return EnrollmentRepository()
        if name == "announcement":
            return AnnouncementRepository()
        if name == "notification":
            return NotificationRepository()
        raise ValueError(f"Unknown repository: {name}")