from repositories.repository_factory import RepositoryFactory
from services.notification_service import NotificationService
from repositories.enrollment_repository import EnrollmentRepository

class AnnouncementService:
    def __init__(self):
        self.announcement_repo = RepositoryFactory.get("announcement")
        self.course_repo = RepositoryFactory.get("course")
        self.enrollment_repo = EnrollmentRepository()
        self.notification_service = NotificationService()

    def create_announcement(self, course_id, teacher_id, title, content):
        """Create a new announcement with business logic"""
        # Validate course exists
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return False, "Course not found"
        
        # Validate teacher owns the course
        if course.teacher_id != teacher_id:
            return False, "Unauthorized: You don't own this course"
        
        # Validate title
        if not title or not title.strip():
            return False, "Title is required"
        
        if len(title.strip()) > 200:
            return False, "Title is too long (max 200 characters)"
        
        # Validate content
        if not content or not content.strip():
            return False, "Content is required"
        
        if len(content.strip()) > 5000:
            return False, "Content is too long (max 5000 characters)"
        
        # Create announcement
        self.announcement_repo.create_announcement(course_id, teacher_id, title.strip(), content.strip())
        
        # Notify enrolled students
        students = self.enrollment_repo.get_enrolled_students(course_id)
        for student_row in students:
            student_id = student_row[0] if isinstance(student_row, tuple) else student_row.get('user_id')
            self.notification_service.create_notification(
                student_id,
                f"New announcement: {title} in {course.title}",
                "announcement",
                None
            )
        
        return True, "Announcement created successfully"

    def get_announcements_by_course(self, course_id):
        """Get all announcements for a course"""
        return self.announcement_repo.get_by_course(course_id)

    def get_announcement_by_id(self, announcement_id):
        """Get announcement by ID"""
        return self.announcement_repo.get_by_id(announcement_id)

