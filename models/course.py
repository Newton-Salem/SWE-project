from models import row_to_dict

class Course:
    def __init__(self, course_id, teacher_id, title, code, description):
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.title = title
        self.code = code
        self.description = description

    @classmethod
    def from_row(cls, cursor, row):
        data = row_to_dict(cursor, row)
        if not data:
            return None
        return cls(
            course_id=data.get("course_id"),
            teacher_id=data.get("teacher_id"),
            title=data.get("title"),
            code=data.get("code"),
            description=data.get("description"),
        )