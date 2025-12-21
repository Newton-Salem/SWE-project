from repositories.repository_factory import RepositoryFactory
from repositories.enrollment_repository import EnrollmentRepository
from services.notification_service import NotificationService


class AnnouncementService:
    def __init__(self):
        self.announcement_repo = RepositoryFactory.get("announcement")
        self.course_repo = RepositoryFactory.get("course")
        self.enrollment_repo = EnrollmentRepository()
        self.notification_service = NotificationService()


    # CREATE ANNOUNCEMENT


    def create_announcement(self, course_id, teacher_id, title, content):
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return False, "Course not found"

        if course.teacher_id != teacher_id:
            return False, "Unauthorized"

        title = title.strip()
        content = content.strip()

        if not title:
            return False, "Title is required"

        if not content:
            return False, "Content is required"

        # Save announcement
        self.announcement_repo.create_announcement(
            course_id=course_id,
            teacher_id=teacher_id,
            title=title,
            content=content
        )

        # Notify students
        students = self.enrollment_repo.get_enrolled_students(course_id)
        for student in students:
            self.notification_service.create_notification(
                user_id=student.user_id,
                message=f"New announcement in {course.title}: {title}",
                notification_type="announcement",
                reference_id=None
            )

        return True, "Announcement created successfully"

    # GET COURSE FOR TEACHER (AUTH CHECK)


    def get_course_for_teacher(self, course_id, teacher_id):
        course = self.course_repo.get_by_id(course_id)
        if not course or course.teacher_id != teacher_id:
            return None
        return course

    # GET COURSE + ANNOUNCEMENTS

    def get_course_announcements(self, course_id):
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return None, []

        announcements = self.announcement_repo.get_by_course(course_id)
        return course, announcements

    # GET ANNOUNCEMENT BY ID

    def get_announcement_by_id(self, announcement_id):
        return self.announcement_repo.get_by_id(announcement_id)
