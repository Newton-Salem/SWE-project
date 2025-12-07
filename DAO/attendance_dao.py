from database.db import MySQLConnection
from datetime import date

class AttendanceDAO:
    def __init__(self):
        db = MySQLConnection()
        self.conn = db.get_connection()
        self.cursor = db.get_cursor()

    def mark_attendance(self, course_id, student_id, status, day=None):
        if day is None:
            day = date.today()
        query = """
            INSERT INTO attendance (course_id, student_id, date, status)
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (course_id, student_id, day, status))
        self.conn.commit()

    def get_attendance_for_course(self, course_id):
        self.cursor.execute("""
            SELECT a.*, u.name AS student_name 
            FROM attendance a
            JOIN users u ON a.student_id = u.user_id
            WHERE a.course_id=?
        """, (course_id,))
        return self.cursor.fetchall()

    def get_attendance_for_student(self, student_id):
        self.cursor.execute("SELECT * FROM attendance WHERE student_id=?", (student_id,))
        return self.cursor.fetchall()