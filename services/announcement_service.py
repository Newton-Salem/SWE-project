from repositories.repository_factory import RepositoryFactory
from repositories.enrollment_repository import EnrollmentRepository
from services.notification_service import NotificationService


class AnnouncementService:
    def __init__(self):
        self.announcement_repo = RepositoryFactory.get("announcement")
        self.course_repo = RepositoryFactory.get("course")
        self.enrollment_repo = EnrollmentRepository()
        self.notification_service = NotificationService()

    # ==================================================
    # CREATE ANNOUNCEMENT (TEACHER)
    # ==================================================
    def create_announcement(self, course_id, teacher_id, title, content):
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return False, "Course not found"

        if course.teacher_id != teacher_id:
            return False, "Unauthorized"

        if not title or not title.strip():
            return False, "Title is required"

        if not content or not content.strip():
            return False, "Content is required"

        # ---------- Save announcement ----------
        self.announcement_repo.create_announcement(
            course_id,
            teacher_id,
            title.strip(),
            content.strip()
        )

        # ---------- Notify students ----------
        students = self.enrollment_repo.get_enrolled_students(course_id)

        for row in students:
            self.notification_service.create_notification(
                row.user_id,
                f"New announcement in {course.title}: {title}",
                "announcement",
                None
            )

        return True, "Announcement created successfully"

    # ==================================================
    # GET ANNOUNCEMENTS BY COURSE
    # ==================================================
    def get_announcements_by_course(self, course_id):
        return self.announcement_repo.get_by_course(course_id)

    # ==================================================
    # GET ANNOUNCEMENT BY ID
    # ==================================================
    def get_announcement_by_id(self, announcement_id):
        return self.announcement_repo.get_by_id(announcement_id)
