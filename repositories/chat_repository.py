from repositories.base_repository import BaseRepository
from models.chatmessage import ChatMessage
from datetime import datetime

class ChatRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def add_message(self, course_id, sender_id, message):
        self.cursor.execute("""
            INSERT INTO chat_messages (course_id, sender_id, message, timestamp)
            VALUES (?, ?, ?, ?)
        """, (course_id, sender_id, message, datetime.now()))
        self.conn.commit()

    def get_messages(self, course_id, limit=100):
        self.cursor.execute("""
            SELECT cm.*, u.name as sender_name, u.role as sender_role
            FROM chat_messages cm
            JOIN users u ON cm.sender_id = u.user_id
            WHERE cm.course_id = ?
            ORDER BY cm.timestamp ASC
            LIMIT ?
        """, (course_id, limit))
        return self.cursor.fetchall()

    def get_recent_messages(self, course_id, count=10):
        self.cursor.execute("""
            SELECT cm.*, u.name as sender_name, u.role as sender_role
            FROM chat_messages cm
            JOIN users u ON cm.sender_id = u.user_id
            WHERE cm.course_id = ?
            ORDER BY cm.timestamp DESC
            LIMIT ?
        """, (course_id, count))
        return self.cursor.fetchall()

