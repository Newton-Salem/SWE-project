# services/course_service.py
from repositories.repository_factory import RepositoryFactory
from repositories.enrollment_repository import EnrollmentRepository
from datetime import date
import re

class CourseService:
    def __init__(self):
        self.course_repo = RepositoryFactory.get("course")
        self.enrollment_repo = EnrollmentRepository()
        self.user_repo = RepositoryFactory.get("user")

    def create_course(self, teacher_id, title, code, description):
        """Create a new course with business logic validation"""
        # Validate teacher exists
        teacher = self.user_repo.get_by_id(teacher_id)
        if not teacher or teacher.role != "teacher":
            return False, "Invalid teacher"
        
        # Validate title
        if not title or not title.strip():
            return False, "Course title is required"
        
        if len(title.strip()) > 200:
            return False, "Course title is too long (max 200 characters)"
        
        # Validate code
        if code:
            code = code.strip().upper()
            # Validate code format (alphanumeric, 3-20 chars)
            if not re.match(r'^[A-Z0-9]{3,20}$', code):
                return False, "Course code must be 3-20 alphanumeric characters"
        else:
            # Generate code if not provided
            import random
            import string
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        # Check if code already exists
        existing = self.course_repo.get_by_code(code)
        if existing:
            return False, "Course code already exists. Please choose a different code."
        
        # Validate description length
        if description and len(description) > 2000:
            return False, "Description is too long (max 2000 characters)"
        
        # Create course
        self.course_repo.create_course(teacher_id, title.strip(), code, description.strip() if description else "")
        return True, f"Course created successfully with code: {code}"

    def get_teacher_courses(self, teacher_id):
        """Get all courses for a teacher"""
        return self.course_repo.get_by_teacher(teacher_id)

    def get_student_courses(self, student_id):
        """Get all courses for a student"""
        return self.course_repo.get_for_student(student_id)

    def get_course_by_id(self, course_id):
        """Get course by ID"""
        return self.course_repo.get_by_id(course_id)

    def join_course(self, student_id, code):
        """Join a course with business logic validation"""
        # Validate student exists
        student = self.user_repo.get_by_id(student_id)
        if not student or student.role != "student":
            return False, "Invalid student"
        
        # Validate code format
        if not code or not code.strip():
            return False, "Course code is required"
        
        code = code.strip().upper()
        
        # Find course by code
        course = self.course_repo.get_by_code(code)
        if not course:
            return False, "Invalid course code"
        
        # Check if already enrolled
        if self.enrollment_repo.is_enrolled(student_id, course.course_id):
            return False, "Already enrolled in this course"
        
        # Enroll student
        self.enrollment_repo.enroll_student(student_id, course.course_id, date.today())
        return True, f"Successfully joined course: {course.title}"
