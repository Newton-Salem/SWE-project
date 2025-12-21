from repositories.base_repository import BaseRepository
from datetime import datetime
from models.submission import Submission

class SubmissionRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def submit(self, assignment_id, student_id, file_path):
        self.cursor.execute("""
            INSERT INTO submissions (assignment_id, student_id, file_path, timestamp)
            VALUES (?, ?, ?, ?)
        """, (assignment_id, student_id, file_path, datetime.now()))
        self.conn.commit()

    def get_by_assignment(self, assignment_id):
        self.cursor.execute("SELECT * FROM submissions WHERE assignment_id = ?", (assignment_id,))
        rows = self.cursor.fetchall()
        return [Submission.from_row(self.cursor, r) for r in rows]

    def get_by_student_and_assignment(self, student_id, assignment_id):
        self.cursor.execute("""
            SELECT * FROM submissions 
            WHERE student_id = ? AND assignment_id = ?
        """, (student_id, assignment_id))
        row = self.cursor.fetchone()
        return Submission.from_row(self.cursor, row)

    def get_by_id(self, submission_id):
        self.cursor.execute("SELECT * FROM submissions WHERE submission_id = ?", (submission_id,))
        row = self.cursor.fetchone()
        return Submission.from_row(self.cursor, row)

    def update_grade(self, submission_id, grade, feedback):
        self.cursor.execute("""
            UPDATE submissions 
            SET grade = ?, feedback = ?
            WHERE submission_id = ?
        """, (grade, feedback, submission_id))
        self.conn.commit()

    def grade_submission(self, submission_id, grade, feedback):
        self.cursor.execute("""
            UPDATE submissions
            SET grade = ?, feedback = ?
            WHERE submission_id = ?
        """, (grade, feedback, submission_id))
        self.conn.commit()

    def get_student_submission(self, assignment_id, student_id):
     self.cursor.execute("""
        SELECT *
        FROM submissions
        WHERE assignment_id = ? AND student_id = ?
    """, (assignment_id, student_id))

     return self.cursor.fetchone()