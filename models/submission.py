class Submission:
    def __init__(self, submission_id, assignment_id, student_id, file_path, timestamp, grade, feedback):
        self.submission_id = submission_id
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.file_path = file_path
        self.timestamp = timestamp
        self.grade = grade
        self.feedback = feedback

    @classmethod
    def from_row(cls, cursor, row):
        if not row:
            return None
        cols = [c[0] for c in cursor.description]
        data = dict(zip(cols, row))
        return cls(
            submission_id=data.get("submission_id"),
            assignment_id=data.get("assignment_id"),
            student_id=data.get("student_id"),
            file_path=data.get("file_path"),
            timestamp=data.get("timestamp"),
            grade=data.get("grade"),
            feedback=data.get("feedback"),
        )
