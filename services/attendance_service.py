from repositories.repository_factory import RepositoryFactory
from datetime import date
from repositories.enrollment_repository import EnrollmentRepository

class AttendanceService:
    def __init__(self):
        self.attendance_repo = RepositoryFactory.get("attendance")
        self.enrollment_repo = EnrollmentRepository()
        self.course_repo = RepositoryFactory.get("course")
        self.user_repo = RepositoryFactory.get("user")

    def get_students_for_attendance(self, course_id):
        """Get all enrolled students for attendance recording"""
        # Validate course exists
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return None
        
        # Get enrolled students
        students = self.attendance_repo.get_students_in_course(course_id)
        return students

    def record_attendance(self, course_id, attendance_data, attendance_date=None):
        """Record attendance for multiple students with business logic"""
        if attendance_date is None:
            attendance_date = date.today()
        
        # Validate course exists
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return False, "Course not found"
        
        # Validate all students are enrolled
        enrolled_students = self.enrollment_repo.get_enrolled_students(course_id)
        enrolled_ids = {row[0] if isinstance(row, tuple) else row.get('user_id') for row in enrolled_students}
        
        # Validate attendance data
        valid_statuses = ['Present', 'Absent', 'Excused']
        for student_id, status in attendance_data.items():
            if int(student_id) not in enrolled_ids:
                return False, f"Student {student_id} is not enrolled in this course"
            if status not in valid_statuses:
                return False, f"Invalid status: {status}. Must be one of {valid_statuses}"
        
        # Record attendance
        for student_id, status in attendance_data.items():
            # Check if already recorded for this date
            existing = self.get_attendance_record(course_id, int(student_id), attendance_date)
            if existing:
                # Update existing record
                self.attendance_repo.update_attendance(course_id, int(student_id), attendance_date, status)
            else:
                # Create new record
                self.attendance_repo.mark_attendance(course_id, int(student_id), attendance_date, status)
        
        return True, "Attendance recorded successfully"

    def get_attendance_record(self, course_id, student_id, attendance_date):
        """Get attendance record for a specific student and date"""
        # This would need to be implemented in repository
        # For now, return None
        return None

    def get_student_attendance_summary(self, course_id, student_id):
        """Get attendance summary for a student in a course"""
        # Get all attendance records
        # This would need a new repository method
        # For now, return basic info
        return {
            'course_id': course_id,
            'student_id': student_id,
            'total_sessions': 0,
            'present_count': 0,
            'absent_count': 0,
            'excused_count': 0,
            'attendance_percentage': 0.0
        }

    def get_course_attendance_summary(self, course_id):
        """Get attendance summary for all students in a course"""
        students = self.get_students_for_attendance(course_id)
        summary = []
        
        for student_row in students:
            student_id = student_row[0] if isinstance(student_row, tuple) else student_row.get('user_id')
            student_name = student_row[1] if isinstance(student_row, tuple) else student_row.get('name')
            
            student_summary = self.get_student_attendance_summary(course_id, student_id)
            student_summary['student_name'] = student_name
            summary.append(student_summary)
        
        return summary

