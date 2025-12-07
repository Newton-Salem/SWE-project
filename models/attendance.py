
class Attendance:
    def __init__(self, attendance_id, course_id, student_id, date, status):
        self.attendance_id = attendance_id
        self.course_id = course_id
        self.student_id = student_id
        self.date = date
        self.status = status

    @classmethod
    def from_row(cls, cursor, row):
        if not row:
            return None
        cols = [c[0] for c in cursor.description]
        data = dict(zip(cols, row))
        return cls(
            attendance_id=data.get("attendance_id"),
            course_id=data.get("course_id"),
            student_id=data.get("student_id"),
            date=data.get("date"),
            status=data.get("status"),
        )
