from repositories.base_repository import BaseRepository
from models.lecture import Lecture


class LectureRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    #  CREATE 
    def add_lecture(self, course_id, title, file_path, video_link, upload_date):
        self.cursor.execute("""
            INSERT INTO lectures (course_id, title, file_path, video_link, upload_date)
            VALUES (?, ?, ?, ?, ?)
        """, (course_id, title, file_path, video_link, upload_date))
        self.conn.commit()

    # READ 
    def get_by_course(self, course_id):
        self.cursor.execute("""
            SELECT * FROM lectures
            WHERE course_id = ?
        """, (course_id,))
        rows = self.cursor.fetchall()
        return [Lecture.from_row(self.cursor, r) for r in rows]

    def get_by_id(self, lecture_id):
        self.cursor.execute("""
            SELECT * FROM lectures
            WHERE lecture_id = ?
        """, (lecture_id,))
        row = self.cursor.fetchone()
        return Lecture.from_row(self.cursor, row) if row else None

    #UPDATE 
    def update(self, lecture_id, title, video_link):
        self.cursor.execute("""
            UPDATE lectures
            SET title = ?, video_link = ?
            WHERE lecture_id = ?
        """, (title, video_link, lecture_id))
        self.conn.commit()

    #DELETE
    def delete(self, lecture_id):
        self.cursor.execute("""
            DELETE FROM lectures
            WHERE lecture_id = ?
        """, (lecture_id,))
        self.conn.commit()
