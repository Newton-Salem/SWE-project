from repositories.base_repository import BaseRepository
from datetime import datetime

class AnnouncementRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def create_announcement(self, course_id, teacher_id, title, content):
        """Create a new announcement"""
        self.cursor.execute("""
            INSERT INTO announcements (course_id, teacher_id, title, content, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (course_id, teacher_id, title, content, datetime.now()))
        self.conn.commit()

    def get_by_course(self, course_id):
        """Get all announcements for a course"""
        self.cursor.execute("""
            SELECT a.*, u.name as teacher_name
            FROM announcements a
            JOIN users u ON a.teacher_id = u.user_id
            WHERE a.course_id = ?
            ORDER BY a.created_at DESC
        """, (course_id,))
        return self.cursor.fetchall()

    def get_by_id(self, announcement_id):
        """Get announcement by ID"""
        self.cursor.execute("""
            SELECT a.*, u.name as teacher_name
            FROM announcements a
            JOIN users u ON a.teacher_id = u.user_id
            WHERE a.announcement_id = ?
        """, (announcement_id,))
        return self.cursor.fetchone()

