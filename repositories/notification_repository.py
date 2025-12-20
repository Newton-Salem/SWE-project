from repositories.base_repository import BaseRepository
from datetime import datetime


class NotificationRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def create(self, user_id, message, notif_type, ref_id):
        self.cursor.execute("""
            INSERT INTO notifications (user_id, message, type, ref_id, created_at, is_read)
            VALUES (?, ?, ?, ?, ?, 0)
        """, (user_id, message, notif_type, ref_id, datetime.now()))
        self.conn.commit()

    def get_by_user(self, user_id):
        self.cursor.execute("""
            SELECT *
            FROM notifications
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        return self.cursor.fetchall()
