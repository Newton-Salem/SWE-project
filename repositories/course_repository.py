
from repositories.base_repository import BaseRepository
from models.course import Course

class CourseRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def create_course(self, teacher_id, title, code, description):
        self.cursor.execute("""
            INSERT INTO courses (teacher_id, title, code, description)
            VALUES (?, ?, ?, ?)
        """, (teacher_id, title, code, description))
        self.conn.commit()

    def get_by_teacher(self, teacher_id):
        self.cursor.execute("SELECT * FROM courses WHERE teacher_id = ?", (teacher_id,))
        rows = self.cursor.fetchall()
        return [Course.from_row(self.cursor, r) for r in rows]

    def get_by_code(self, code):
        self.cursor.execute("SELECT * FROM courses WHERE code = ?", (code,))
        row = self.cursor.fetchone()
        return Course.from_row(self.cursor, row)

    def get_for_student(self, student_id):
        self.cursor.execute("""
            SELECT c.*
            FROM courses c
            JOIN enrollment e ON e.course_id = c.course_id
            WHERE e.student_id = ?
        """, (student_id,))
        rows = self.cursor.fetchall()
        return [Course.from_row(self.cursor, r) for r in rows]

    def get_by_id(self, course_id):
        self.cursor.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
        row = self.cursor.fetchone()
        return Course.from_row(self.cursor, row)