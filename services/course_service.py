# services/course_service.py
from repositories.repository_factory import RepositoryFactory
from database.connection import MySQLConnection
from datetime import date

class CourseService:
    def __init__(self):
        self.course_repo = RepositoryFactory.get("course")

    def create_course(self, teacher_id, title, code, description):
        self.course_repo.create_course(teacher_id, title, code, description)

    def get_teacher_courses(self, teacher_id):
        return self.course_repo.get_by_teacher(teacher_id)

    def get_student_courses(self, student_id):
        return self.course_repo.get_for_student(student_id)

    def join_course(self, student_id, code):
        course = self.course_repo.get_by_code(code)
        if not course:
            return False, "Invalid course code"

        db = MySQLConnection()
        cur = db.get_cursor()
        cur.execute("""
            INSERT INTO enrollment (student_id, course_id, enrolled_date)
            VALUES (?, ?, ?)
        """, (student_id, course.course_id, date.today()))
        db.get_connection().commit()
        return True, "Joined course"
