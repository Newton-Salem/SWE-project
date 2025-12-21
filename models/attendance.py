from models import row_to_dict

class Attendance:
    def __init__(self, attendance_id, course_id, student_id, date, status):
        self.attendance_id = attendance_id
        self.course_id = course_id
        self.student_id = student_id
        self.date = date
        self.status = status

    @classmethod
    def from_row(cls, cursor, row):
        data = row_to_dict(cursor, row)
        if not data:
            return None
        return cls(
            attendance_id=data.get("attendance_id"),
            course_id=data.get("course_id"),
            student_id=data.get("student_id"),
            date=data.get("date"),
            status=data.get("status"),
        )