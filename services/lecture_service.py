from repositories.repository_factory import RepositoryFactory
from services.notification_service import NotificationService
from datetime import date
import os
import uuid

class LectureService:
    def __init__(self):
        self.lecture_repo = RepositoryFactory.get("lecture")
        self.course_repo = RepositoryFactory.get("course")
        self.notification_service = NotificationService()

    def upload_lecture(self, course_id, title, file_path, video_link, upload_folder, max_file_size=10*1024*1024):
        """Upload a lecture with business logic validation"""
        # Validate course exists
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return False, "Course not found"
        
        # Validate title
        if not title or not title.strip():
            return False, "Title is required"
        
        # Validate at least file or video link provided
        if not file_path and not video_link:
            return False, "Either a file or video link must be provided"
        
        # Validate file if provided
        if file_path:
            if not os.path.exists(file_path):
                return False, "File not found"
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > max_file_size:
                return False, f"File size exceeds {max_file_size / (1024*1024)}MB limit"
            
            # Validate file extension (only PDF allowed)
            if not file_path.lower().endswith('.pdf'):
                return False, "Only PDF files are allowed"
        
        # Validate video link format if provided
        if video_link and not video_link.strip().startswith(('http://', 'https://')):
            return False, "Invalid video link format. Must start with http:// or https://"
        
        # Save lecture
        self.lecture_repo.add_lecture(course_id, title, file_path, video_link, date.today())
        
        # Notify enrolled students
        from repositories.enrollment_repository import EnrollmentRepository
        enrollment_repo = EnrollmentRepository()
        students = enrollment_repo.get_enrolled_students(course_id)
        for student_row in students:
            student_id = student_row[0] if isinstance(student_row, tuple) else student_row.get('user_id')
            self.notification_service.create_notification(
                student_id,
                f"New lecture '{title}' uploaded in {course.title}",
                "lecture",
                None
            )
        
        return True, "Lecture uploaded successfully"

    def get_lectures_by_course(self, course_id):
        """Get all lectures for a course"""
        return self.lecture_repo.get_by_course(course_id)

    def get_lecture_by_id(self, lecture_id):
        """Get lecture by ID"""
        return self.lecture_repo.get_by_id(lecture_id)

    def save_uploaded_file(self, file, upload_folder):
        """Save uploaded file with unique filename"""
        os.makedirs(upload_folder, exist_ok=True)
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path

