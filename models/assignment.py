from models import row_to_dict

class Assignment:
    def __init__(self, assignment_id, course_id, title, description, due_date, max_grade):
        self.assignment_id = assignment_id
        self.course_id = course_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.max_grade = max_grade

    @classmethod
    def from_row(cls, cursor, row):
        data = row_to_dict(cursor, row)
        if not data:
            return None
        return cls(
            assignment_id=data.get("assignment_id"),
            course_id=data.get("course_id"),
            title=data.get("title"),
            description=data.get("description"),
            due_date=data.get("due_date"),
            max_grade=data.get("max_grade"),
        )
