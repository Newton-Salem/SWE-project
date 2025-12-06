class Attendance:
    def _init_(self, attendance_id, course_id, student_id, date, status):
        self.attendance_id = attendance_id
        self.course_id = course_id
        self.student_id = student_id
        self.date = date
        self.status = status