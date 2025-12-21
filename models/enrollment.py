from models import row_to_dict

class Enrollment:
    def __init__(self, id, student_id, course_id, enrolled_date):
        self.id = id
        self.student_id = student_id
        self.course_id = course_id
        self.enrolled_date = enrolled_date

    @classmethod
    def from_row(cls, cursor, row):
        data = row_to_dict(cursor, row)
        if not data:
            return None
        return cls(
            id=data.get("id"),
            student_id=data.get("student_id"),
            course_id=data.get("course_id"),
            enrolled_date=data.get("enrolled_date"),
        )