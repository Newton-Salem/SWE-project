from repositories.repository_factory import RepositoryFactory

class ChatService:
    def __init__(self):
        self.chat_repo = RepositoryFactory.get("chat")

    def send_message(self, course_id, student_id, sender_id, message):
        if not message.strip():
            return False, "Message cannot be empty"

        self.chat_repo.add_message(
            course_id,
            student_id,
            sender_id,
            message.strip()
        )
        return True, "Message sent"

    def get_student_chat(self, course_id, student_id):
        return self.chat_repo.get_student_chat(course_id, student_id)

    def get_students_with_chats(self, course_id):
        return self.chat_repo.get_students_with_chats(course_id)
