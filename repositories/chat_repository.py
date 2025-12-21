from repositories.base_repository import BaseRepository
from datetime import datetime

class ChatRepository(BaseRepository):

    def add_message(self, course_id, student_id, sender_id, message):
        self.cursor.execute("""
            INSERT INTO chat_messages
            (course_id, student_id, sender_id, message, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (course_id, student_id, sender_id, message, datetime.now()))
        self.conn.commit()

    def get_student_chat(self, course_id, student_id):
        self.cursor.execute("""
            SELECT cm.message,
                   cm.timestamp,
                   u.name AS sender_name
            FROM chat_messages cm
            JOIN users u ON cm.sender_id = u.user_id
            WHERE cm.course_id = ?
              AND cm.student_id = ?
            ORDER BY cm.timestamp
        """, (course_id, student_id))
        return self.cursor.fetchall()

    def get_students_with_chats(self, course_id):
        self.cursor.execute("""
            SELECT DISTINCT u.user_id, u.name
            FROM chat_messages cm
            JOIN users u ON cm.student_id = u.user_id
            WHERE cm.course_id = ?
        """, (course_id,))
        return self.cursor.fetchall()