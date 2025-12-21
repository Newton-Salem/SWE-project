from repositories.base_repository import BaseRepository

class AttendanceRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    # ---------- INSERT ----------
    def mark_attendance(self, course_id, student_id, date, status):
        self.cursor.execute("""
            INSERT INTO attendance (course_id, student_id, date, status)
            VALUES (?, ?, ?, ?)
        """, (course_id, student_id, date, status))
        self.conn.commit()

    # ---------- UPDATE ----------
    def update_attendance(self, course_id, student_id, date, status):
        self.cursor.execute("""
            UPDATE attendance
            SET status = ?
            WHERE course_id = ? AND student_id = ? AND date = ?
        """, (status, course_id, student_id, date))
        self.conn.commit()

    # ---------- GET ONE ----------
    def get_attendance(self, course_id, student_id, date):
        self.cursor.execute("""
            SELECT *
            FROM attendance
            WHERE course_id = ? AND student_id = ? AND date = ?
        """, (course_id, student_id, date))
        return self.cursor.fetchone()

    # ---------- GET STUDENTS ----------
    def get_students_in_course(self, course_id):
        self.cursor.execute("""
            SELECT u.user_id, u.name
            FROM users u
            JOIN enrollment e ON u.user_id = e.student_id
            WHERE e.course_id = ?
        """, (course_id,))
        return self.cursor.fetchall()

    # ---------- STUDENT ATTENDANCE ----------
    def get_student_attendance(self, course_id, student_id):
        self.cursor.execute("""
            SELECT date, status
            FROM attendance
            WHERE course_id = ? AND student_id = ?
            ORDER BY date
        """, (course_id, student_id))
        return self.cursor.fetchall()
