from database.db import MySQLConnection
from datetime import date

class LectureDAO:
    def _init_(self):
        self.db = MySQLConnection()
        self.cursor = self.db.get_cursor()

    def add_lecture(self, course_id, title, file_path=None, video_link=None):
        query = """
            INSERT INTO lectures (course_id, title, file_path, video_link, upload_date)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(
            query, (course_id, title, file_path, video_link, date.today())
        )
        self.db.get_connection().commit()
        return self.cursor.lastrowid

    def get_lectures(self, course_id):
        self.cursor.execute("SELECT * FROM lectures WHERE course_id=%s", (course_id,))
        return self.cursor.fetchall()