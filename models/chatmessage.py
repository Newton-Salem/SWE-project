class ChatMessage:
    def __init__(self, chat_id, course_id, sender_id, message, timestamp):
        self.chat_id = chat_id
        self.course_id = course_id
        self.sender_id = sender_id
        self.message = message
        self.timestamp = timestamp