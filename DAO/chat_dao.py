from database.db import MySQLConnection
from datetime import datetime

class ChatDAO:
    def _init_(self):
        db = MySQLConnection()
        self.conn = db.get_connection()
        self.cursor = db.get_cursor()

    def add_message(self, course_id, sender_id, message):
        now = datetime.now()
        query = """
            INSERT INTO chat_messages (course_id, sender_id, message, timestamp)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (course_id, sender_id, message, now))
        self.conn.commit()

    def get_messages(self, course_id):
        self.cursor.execute("""
            SELECT c.*, u.name AS sender_name
            FROM chat_messages c
            JOIN users u ON c.sender_id = u.user_id
            WHERE course_id=%s
            ORDER BY timestamp ASC
        """, (course_id,))
        return self.cursor.fetchall()