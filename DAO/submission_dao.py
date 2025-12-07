from database.db import MySQLConnection
from datetime import datetime

class SubmissionDAO:
    def __init__(self):
        db = MySQLConnection()
        self.conn = db.get_connection()
        self.cursor = db.get_cursor()

    def submit_assignment(self, assignment_id, student_id, file_path):
        now = datetime.now()
        query = """
            INSERT INTO submissions (assignment_id, student_id, file_path, timestamp)
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (assignment_id, student_id, file_path, now))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_submissions_for_assignment(self, assignment_id):
        self.cursor.execute("""
            SELECT s.*, u.name AS student_name FROM submissions s
            JOIN users u ON s.student_id = u.user_id
            WHERE assignment_id=?
        """, (assignment_id,))
        return self.cursor.fetchall()

    def grade_submission(self, submission_id, grade, feedback):
        query = """
            UPDATE submissions SET grade=?, feedback=?
            WHERE submission_id=?
        """
        self.cursor.execute(query, (grade, feedback, submission_id))
        self.conn.commit()

    def get_student_submissions(self, student_id):
        self.cursor.execute("SELECT * FROM submissions WHERE student_id=?", (student_id,))
        return self.cursor.fetchall()