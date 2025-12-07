class ChatMessage:
    def __init__(self, chat_id, course_id, sender_id, message, timestamp):
        self.chat_id = chat_id
        self.course_id = course_id
        self.sender_id = sender_id
        self.message = message
        self.timestamp = timestamp

    @classmethod
    def from_row(cls, cursor, row):
        if not row:
            return None
        cols = [c[0] for c in cursor.description]
        data = dict(zip(cols, row))
        return cls(
            chat_id=data.get("chat_id"),
            course_id=data.get("course_id"),
            sender_id=data.get("sender_id"),
            message=data.get("message"),
            timestamp=data.get("timestamp"),
        )
