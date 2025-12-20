
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
    
    def update_course(self, course_id, title, description):
        self.cursor.execute("""
            UPDATE courses
            SET title = ?, description = ?
            WHERE course_id = ?
        """, (title, description, course_id))
        self.conn.commit()

    def delete(self, course_id):
     self.cursor.execute(
            "DELETE FROM courses WHERE course_id = ?",
            (course_id,)
        )
     self.conn.commit()
    
    def get_all(self):
     self.cursor.execute("SELECT * FROM courses")
     rows = self.cursor.fetchall()
     return rows
    