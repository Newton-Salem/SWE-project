from datetime import date
from repositories.repository_factory import RepositoryFactory
from repositories.enrollment_repository import EnrollmentRepository

class AttendanceService:
    def __init__(self):
        self.attendance_repo = RepositoryFactory.get("attendance")
        self.enrollment_repo = EnrollmentRepository()
        self.course_repo = RepositoryFactory.get("course")

    
    # TEACHER: GET STUDENTS
    
    def get_students_for_attendance(self, course_id):
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return None
        return self.attendance_repo.get_students_in_course(course_id)

    
    # TEACHER: RECORD ATTENDANCE
   
    def record_attendance(self, course_id, attendance_data, attendance_date=None):
        if attendance_date is None:
            attendance_date = date.today()

        course = self.course_repo.get_by_id(course_id)
        if not course:
            return False, "Course not found"

        enrolled_students = self.enrollment_repo.get_enrolled_students(course_id)
        enrolled_ids = {row.user_id for row in enrolled_students}

        valid_statuses = ["Present", "Absent", "Excused"]

        for student_id, status in attendance_data.items():
            student_id = int(student_id)

            if student_id not in enrolled_ids:
                return False, "Student not enrolled"

            if status not in valid_statuses:
                return False, "Invalid status"

        for student_id, status in attendance_data.items():
            student_id = int(student_id)

            existing = self.attendance_repo.get_attendance(
                course_id, student_id, attendance_date
            )

            if existing:
                self.attendance_repo.update_attendance(
                    course_id, student_id, attendance_date, status
                )
            else:
                self.attendance_repo.mark_attendance(
                    course_id, student_id, attendance_date, status
                )

        return True, "Attendance recorded successfully"

   
    #  STUDENT: VIEW ATTENDANCE
   
    def get_attendance_for_student(self, course_id, student_id):
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return None

        return self.attendance_repo.get_student_attendance(
            course_id, student_id
        )