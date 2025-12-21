from repositories.base_repository import BaseRepository
from datetime import date

class EnrollmentRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def enroll_student(self, student_id, course_id, enrolled_date):
        self.cursor.execute("""
            INSERT INTO enrollment (student_id, course_id, enrolled_date)
            VALUES (?, ?, ?)
        """, (student_id, course_id, enrolled_date))
        self.conn.commit()

    def is_enrolled(self, student_id, course_id):
        self.cursor.execute("""
            SELECT * FROM enrollment 
            WHERE student_id = ? AND course_id = ?
        """, (student_id, course_id))
        return self.cursor.fetchone() is not None

    def get_enrolled_students(self, course_id):
        self.cursor.execute("""
            SELECT u.* FROM users u
            JOIN enrollment e ON e.student_id = u.user_id
            WHERE e.course_id = ?
        """, (course_id,))
        return self.cursor.fetchall()

    def get_student_courses(self, student_id):
        self.cursor.execute("""
            SELECT c.* FROM courses c
            JOIN enrollment e ON e.course_id = c.course_id
            WHERE e.student_id = ?
        """, (student_id,))
        return self.cursor.fetchall()