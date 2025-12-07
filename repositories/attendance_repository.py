from repositories.base_repository import BaseRepository
from models.attendance import Attendance

class AttendanceRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def mark_attendance(self, course_id, student_id, date, status):
        self.cursor.execute("""
            INSERT INTO attendance (course_id, student_id, date, status)
            VALUES (?, ?, ?, ?)
        """, (course_id, student_id, date, status))
        self.conn.commit()

    def get_students_in_course(self, course_id):
        self.cursor.execute("""
            SELECT u.user_id, u.name
            FROM users u
            JOIN enrollment e ON u.user_id = e.student_id
            WHERE e.course_id = ?
        """, (course_id,))
        rows = self.cursor.fetchall()
        cols = [c[0] for c in self.cursor.description]
        return [dict(zip(cols, r)) for r in rows]
