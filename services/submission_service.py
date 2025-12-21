from repositories.repository_factory import RepositoryFactory
from services.notification_service import NotificationService

class SubmissionService:
    def __init__(self):
        self.submission_repo = RepositoryFactory.get("submission")
        self.assignment_repo = RepositoryFactory.get("assignment")
        self.user_repo = RepositoryFactory.get("user")
        self.course_repo = RepositoryFactory.get("course")
        self.notification_service = NotificationService()

    def get_submission_by_id(self, submission_id):
        """Get submission by ID"""
        return self.submission_repo.get_by_id(submission_id)

    def get_submissions_by_assignment(self, assignment_id):
        """Get all submissions for an assignment with student information"""
        submissions = self.submission_repo.get_by_assignment(assignment_id)
        
        #student names
        for submission in submissions:
            student = self.user_repo.get_by_id(submission.student_id)
            submission.student_name = student.name if student else "Unknown"
            submission.student_email = student.email if student else "Unknown"
        
        return submissions

    def get_submission_with_details(self, submission_id):
        """Get submission with full details (student, assignment, course)"""
        submission = self.submission_repo.get_by_id(submission_id)
        if not submission:
            return None
        
        student = self.user_repo.get_by_id(submission.student_id)
        assignment = self.assignment_repo.get_by_id(submission.assignment_id)
        course = self.course_repo.get_by_id(assignment.course_id) if assignment else None
        
        return {
            'submission': submission,
            'student': student,
            'assignment': assignment,
            'course': course
        }

    def can_submit(self, assignment_id, student_id):
        """Check if student can submit assignment (business logic)"""
        assignment = self.assignment_repo.get_by_id(assignment_id)
        if not assignment:
            return False, "Assignment not found"
        
        # Check if already submitted
        existing = self.submission_repo.get_by_student_and_assignment(student_id, assignment_id)
        if existing:
            return False, "You have already submitted this assignment"
        
        # Check due date
        from datetime import date, datetime
        due_date = datetime.strptime(assignment.due_date, "%Y-%m-%d").date() if isinstance(assignment.due_date, str) else assignment.due_date
        if date.today() > due_date:
            return False, "Assignment due date has passed"
        
        return True, "Can submit"