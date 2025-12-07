from database.db import MySQLConnection
from datetime import datetime

class AssignmentDAO:
    def __init__(self):
        db = MySQLConnection()
        self.conn = db.get_connection()
        self.cursor = db.get_cursor()

    def create_assignment(self, course_id, title, description, due_date, max_grade):
        query = """
            INSERT INTO assignments (course_id, title, description, due_date, max_grade)
            VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (course_id, title, description, due_date, max_grade))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_assignments_for_course(self, course_id):
        self.cursor.execute("SELECT * FROM assignments WHERE course_id=?", (course_id,))
        return self.cursor.fetchall()

    def get_assignment(self, assignment_id):
        self.cursor.execute("SELECT * FROM assignments WHERE assignment_id=?", (assignment_id,))
        return self.cursor.fetchone()