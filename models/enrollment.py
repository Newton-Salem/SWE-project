
class Enrollment:
    def __init__(self, id, student_id, course_id, enrolled_date):
        self.id = id
        self.student_id = student_id
        self.course_id = course_id
        self.enrolled_date = enrolled_date

    @classmethod
    def from_row(cls, cursor, row):
        if not row:
            return None
        cols = [c[0] for c in cursor.description]
        data = dict(zip(cols, row))
        return cls(
            id=data.get("id"),
            student_id=data.get("student_id"),
            course_id=data.get("course_id"),
            enrolled_date=data.get("enrolled_date"),
        )

        self.id = id
        self.student_id = student_id
        self.course_id = course_id
        self.date = date