from database.db import MySQLConnection
from datetime import date

class CourseDAO:
    def _init_(self):
        self.db = MySQLConnection()
        self.cursor = self.db.get_cursor()

    def create_course(self, teacher_id, title, description, code):
        query = """
            INSERT INTO courses (teacher_id, title, code, description)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (teacher_id, title, code, description))
        self.db.get_connection().commit()
        return self.cursor.lastrowid

    def join_course(self, student_id, course_code):
        self.cursor.execute("SELECT course_id FROM courses WHERE code=%s", (course_code,))
        course = self.cursor.fetchone()
        if not course:
            return None

        course_id = course["course_id"]

        self.cursor.execute("""
            SELECT * FROM enrollment 
            WHERE student_id=%s AND course_id=%s
        """, (student_id, course_id))
        exists = self.cursor.fetchone()

        if exists:
            return "already exist"

        self.cursor.execute("""
            INSERT INTO enrollment (student_id, course_id, enrolled_date)
            VALUES (%s, %s, %s)
        """, (student_id, course_id, date.today()))

        self.db.get_connection().commit()
        return "joined the course"

    def get_teacher_courses(self, teacher_id):
        self.cursor.execute("""
            SELECT * FROM courses WHERE teacher_id=%s
        """, (teacher_id,))
        return self.cursor.fetchall()

    def get_student_courses(self, student_id):
        self.cursor.execute("""
        SELECT c.* FROM courses c
        JOIN enrollment e ON c.course_id = e.course_id
        WHERE e.student_id=%s
        """, (student_id,))
        return self.cursor.fetchall()

    def get_course(self, course_id):
        self.cursor.execute("SELECT * FROM courses WHERE course_id=%s", (course_id,))
        return self.cursor.fetchone()