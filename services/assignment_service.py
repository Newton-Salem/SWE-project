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

    # ==================================================
    # CREATE ASSIGNMENT (TEACHER)
    # ==================================================
    def create_assignment(self, course_id, title, description, due_date, max_grade):
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return False, "Course not found"

        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
            if due_date_obj < date.today():
                return False, "Due date cannot be in the past"
        except ValueError:
            return False, "Invalid date format"

        try:
            max_grade = int(max_grade)
            if max_grade <= 0:
                return False, "Invalid max grade"
        except ValueError:
            return False, "Invalid max grade"

        if not title.strip():
            return False, "Title is required"

        self.assignment_repo.create_assignment(
            course_id, title, description, due_date_obj, max_grade
        )

        # Notify students
        from repositories.enrollment_repository import EnrollmentRepository
        enrollment_repo = EnrollmentRepository()
        students = enrollment_repo.get_enrolled_students(course_id)

        for s in students:
            self.notification_service.create_notification(
                s.user_id,
                f"New assignment '{title}' posted in {course.title}",
                "assignment",
                None
            )

        return True, "Assignment created successfully"

    # ==================================================
    # DELETE ASSIGNMENT (TEACHER)
    # ==================================================
    def delete_assignment(self, assignment_id, teacher_id):
        assignment = self.assignment_repo.get_by_id(assignment_id)
        if not assignment:
            return False, "Assignment not found"

        course = self.course_repo.get_by_id(assignment.course_id)
        if not course or course.teacher_id != teacher_id:
            return False, "Unauthorized"

        self.assignment_repo.delete(assignment_id)
        return True, "Assignment deleted successfully"

    # ==================================================
    # READ
    # ==================================================
    def get_assignments_by_course(self, course_id):
        return self.assignment_repo.get_by_course(course_id)

    def get_assignment_by_id(self, assignment_id):
        return self.assignment_repo.get_by_id(assignment_id)

    # ==================================================
    # SUBMIT ASSIGNMENT (STUDENT)
    # ==================================================
    def submit_assignment(self, assignment_id, student_id, file_path):
        assignment = self.assignment_repo.get_by_id(assignment_id)
        if not assignment:
            return False, "Assignment not found"

        if date.today() > assignment.due_date:
            return False, "Deadline passed"

        if self.submission_repo.get_by_student_and_assignment(student_id, assignment_id):
            return False, "Already submitted"

        self.submission_repo.submit(assignment_id, student_id, file_path)

        course = self.course_repo.get_by_id(assignment.course_id)
        self.notification_service.create_notification(
            course.teacher_id,
            f"New submission for '{assignment.title}'",
            "submission",
            assignment_id
        )

        return True, "Submitted successfully"

    # ==================================================
    # VIEW SUBMISSIONS (TEACHER) ✅ الميثود الناقصة
    # ==================================================
    def get_submissions_by_assignment(self, assignment_id):
        submissions = self.submission_repo.get_by_assignment(assignment_id)

        for submission in submissions:
            student = self.user_repo.get_by_id(submission.student_id)
            submission.student_name = student.name if student else "Unknown"

        return submissions

    # ==================================================
    # GRADE SUBMISSION (TEACHER)
    # ==================================================
    def grade_submission(self, submission_id, teacher_id, grade, feedback=None):
        # Get submission
        submission = self.submission_repo.get_by_id(submission_id)
        if not submission:
            return False, "Submission not found"

        # Get assignment
        assignment = self.assignment_repo.get_by_id(submission.assignment_id)
        if not assignment:
            return False, "Assignment not found"

        # Check teacher authorization
        course = self.course_repo.get_by_id(assignment.course_id)
        if not course or course.teacher_id != teacher_id:
            return False, "Unauthorized"

        # Validate grade
        try:
            grade = float(grade)
        except ValueError:
            return False, "Invalid grade"

        if grade < 0 or grade > assignment.max_grade:
            return False, f"Grade must be between 0 and {assignment.max_grade}"

        # Save grade
        self.submission_repo.grade_submission(
            submission_id,
            grade,
            feedback
        )

        # Notify student
        self.notification_service.create_notification(
            submission.student_id,
            f"Your submission for '{assignment.title}' has been graded",
            "grade",
            submission_id
        )

        return True, "Submission graded successfully"
    # ==================================================
    def get_student_assignment_status(self, assignment_id, student_id):
        assignment = self.assignment_repo.get_by_id(assignment_id)
        if not assignment:
            return None

        submission = self.submission_repo.get_student_submission(
            assignment_id,
         student_id
        )

        return {
            "assignment": assignment,
            "submission": submission
        }
    def get_assignments_by_course(self, course_id, student_id=None):
        assignments = self.assignment_repo.get_by_course(course_id)

        for a in assignments:
        # قيم افتراضية
            a.submitted = False
            a.grade = None

        # لو Student
            if student_id:
                submission = self.submission_repo.get_by_student_and_assignment(
                    student_id,
                    a.assignment_id
                )
            if submission:
                a.submitted = True
                a.grade = submission.grade

        return assignments

