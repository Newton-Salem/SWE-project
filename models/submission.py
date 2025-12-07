class Submission:
    def __init__(self, submission_id, assignment_id, student_id, file_path, timestamp, grade, feedback):
        self.submission_id = submission_id
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.file_path = file_path
        self.timestamp = timestamp
        self.grade = grade
        self.feedback = feedback