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
