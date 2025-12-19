from repositories.repository_factory import RepositoryFactory
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.db = RepositoryFactory.get("user").conn
        self.cursor = RepositoryFactory.get("user").cursor

    def create_notification(self, user_id, message, notification_type, related_id=None):
        """Create a notification for a user"""
        self.cursor.execute("""
            INSERT INTO notifications (user_id, message, type, related_id, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, message, notification_type, related_id, datetime.now()))
        self.db.commit()

    def get_user_notifications(self, user_id, unread_only=False):
        """Get notifications for a user"""
        query = """
            SELECT * FROM notifications 
            WHERE user_id = ?
        """
        params = [user_id]
        
        if unread_only:
            query += " AND is_read = 0"
        
        query += " ORDER BY created_at DESC LIMIT 50"
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def mark_as_read(self, notification_id, user_id):
        """Mark a notification as read"""
        self.cursor.execute("""
            UPDATE notifications 
            SET is_read = 1 
            WHERE notification_id = ? AND user_id = ?
        """, (notification_id, user_id))
        self.db.commit()

    def mark_all_as_read(self, user_id):
        """Mark all notifications as read for a user"""
        self.cursor.execute("""
            UPDATE notifications 
            SET is_read = 1 
            WHERE user_id = ? AND is_read = 0
        """, (user_id,))
        self.db.commit()

    def get_unread_count(self, user_id):
        """Get count of unread notifications"""
        self.cursor.execute("""
            SELECT COUNT(*) FROM notifications 
            WHERE user_id = ? AND is_read = 0
        """, (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

