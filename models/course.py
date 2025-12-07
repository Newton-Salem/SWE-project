
class Course:
    def __init__(self, course_id, teacher_id, title, code, description):
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.title = title
        self.code = code
        self.description = description

    @classmethod
    def from_row(cls, cursor, row):
        if not row:
            return None
        cols = [c[0] for c in cursor.description]
        data = dict(zip(cols, row))
        return cls(
            course_id=data.get("course_id"),
            teacher_id=data.get("teacher_id"),
            title=data.get("title"),
            code=data.get("code"),
            description=data.get("description"),
        )
