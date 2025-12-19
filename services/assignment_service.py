from repositories.repository_factory import RepositoryFactory
from datetime import datetime, date
from services.notification_service import NotificationService

class AssignmentService:
    def __init__(self):
        self.assignment_repo = RepositoryFactory.get("assignment")
        self.submission_repo = RepositoryFactory.get("submission")
        self.course_repo = RepositoryFactory.get("course")
        self.user_repo = RepositoryFactory.get("user")
        self.notification_service = NotificationService()

    def create_assignment(self, course_id, title, description, due_date, max_grade):
        """Create a new assignment with business logic validation"""
        # Validate course exists
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return False, "Course not found"
        
        # Validate due date is in the future
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
            if due_date_obj < date.today():
                return False, "Due date cannot be in the past"
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
        
        # Validate max_grade is positive
        try:
            max_grade_int = int(max_grade)
            if max_grade_int <= 0:
                return False, "Maximum grade must be greater than 0"
        except ValueError:
            return False, "Invalid grade value"
        
        # Validate title and description
        if not title or not title.strip():
            return False, "Title is required"
        
        # Create assignment
        self.assignment_repo.create_assignment(
            course_id, title, description, due_date, max_grade_int
        )
        
        # Notify enrolled students (bonus feature)
        from repositories.enrollment_repository import EnrollmentRepository
        enrollment_repo = EnrollmentRepository()
        students = enrollment_repo.get_enrolled_students(course_id)
        for student_row in students:
            student_id = student_row[0] if isinstance(student_row, tuple) else student_row.get('user_id')
            self.notification_service.create_notification(
                student_id,
                f"New assignment '{title}' posted in {course.title}",
                "assignment",
                None
            )
        
        return True, "Assignment created successfully"

    def get_assignments_by_course(self, course_id):
        """Get all assignments for a course"""
        return self.assignment_repo.get_by_course(course_id)

    def get_assignment_by_id(self, assignment_id):
        """Get assignment by ID"""
        return self.assignment_repo.get_by_id(assignment_id)

    def submit_assignment(self, assignment_id, student_id, file_path):
        """Submit an assignment with business logic"""
        # Validate assignment exists
        assignment = self.assignment_repo.get_by_id(assignment_id)
        if not assignment:
            return False, "Assignment not found"
        
        # Check if due date has passed
        due_date = datetime.strptime(assignment.due_date, "%Y-%m-%d").date() if isinstance(assignment.due_date, str) else assignment.due_date
        if date.today() > due_date:
            return False, "Assignment due date has passed"
        
        # Check if already submitted (prevent duplicate submissions)
        existing = self.submission_repo.get_by_student_and_assignment(student_id, assignment_id)
        if existing:
            return False, "You have already submitted this assignment"
        
        # Create submission
        self.submission_repo.submit(assignment_id, student_id, file_path)
        
        # Notify teacher
        course = self.course_repo.get_by_id(assignment.course_id)
        if course:
            self.notification_service.create_notification(
                course.teacher_id,
                f"New submission received for assignment '{assignment.title}'",
                "submission",
                assignment_id
            )
        
        return True, "Assignment submitted successfully"

    def get_submissions_by_assignment(self, assignment_id):
        """Get all submissions for an assignment with student names"""
        submissions = self.submission_repo.get_by_assignment(assignment_id)
        
        # Enrich with student names
        for submission in submissions:
            student = self.user_repo.get_by_id(submission.student_id)
            submission.student_name = student.name if student else "Unknown"
        
        return submissions

    def grade_submission(self, submission_id, grade, feedback, teacher_id):
        """Grade a submission with business logic"""
        # Validate submission exists
        submission = self.submission_repo.get_by_id(submission_id)
        if not submission:
            return False, "Submission not found"
        
        # Validate teacher owns the assignment's course
        assignment = self.assignment_repo.get_by_id(submission.assignment_id)
        if not assignment:
            return False, "Assignment not found"
        
        course = self.course_repo.get_by_id(assignment.course_id)
        if not course or course.teacher_id != teacher_id:
            return False, "Unauthorized: You don't own this course"
        
        # Validate grade
        try:
            grade_int = int(grade)
            if grade_int < 0:
                return False, "Grade cannot be negative"
            if assignment.max_grade and grade_int > assignment.max_grade:
                return False, f"Grade cannot exceed maximum grade of {assignment.max_grade}"
        except ValueError:
            return False, "Invalid grade value"
        
        # Validate feedback
        if not feedback or not feedback.strip():
            return False, "Feedback is required"
        
        # Update grade
        self.submission_repo.update_grade(submission_id, grade_int, feedback)
        
        # Notify student
        self.notification_service.create_notification(
            submission.student_id,
            f"You received a grade of {grade_int}/{assignment.max_grade} for assignment '{assignment.title}'",
            "grade",
            submission_id
        )
        
        return True, "Grade saved successfully"

