from repositories.repository_factory import RepositoryFactory
from repositories.enrollment_repository import EnrollmentRepository

class ChatService:
    def __init__(self):
        self.chat_repo = RepositoryFactory.get("chat")
        self.course_repo = RepositoryFactory.get("course")
        self.enrollment_repo = EnrollmentRepository()
        self.user_repo = RepositoryFactory.get("user")

    def send_message(self, course_id, sender_id, message):
        """Send a chat message with business logic validation"""
        # Validate course exists
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return False, "Course not found"
        
        # Validate sender is enrolled (student) or is teacher
        is_teacher = course.teacher_id == sender_id
        is_enrolled = self.enrollment_repo.is_enrolled(sender_id, course_id) if not is_teacher else False
        
        if not is_teacher and not is_enrolled:
            return False, "You must be enrolled in this course to send messages"
        
        # Validate message
        if not message or not message.strip():
            return False, "Message cannot be empty"
        
        if len(message.strip()) > 1000:
            return False, "Message is too long (max 1000 characters)"
        
        # Send message
        self.chat_repo.add_message(course_id, sender_id, message.strip())
        return True, "Message sent successfully"

    def get_messages(self, course_id, limit=100):
        """Get chat messages for a course with sender information"""
        messages = self.chat_repo.get_messages(course_id, limit)
        
        # Enrich with sender information
        enriched_messages = []
        for msg_row in messages:
            if isinstance(msg_row, tuple):
                # Convert tuple to dict if needed
                msg_dict = {
                    'chat_id': msg_row[0],
                    'course_id': msg_row[1],
                    'sender_id': msg_row[2],
                    'message': msg_row[3],
                    'timestamp': msg_row[4],
                    'sender_name': msg_row[5] if len(msg_row) > 5 else 'Unknown',
                    'sender_role': msg_row[6] if len(msg_row) > 6 else 'Unknown'
                }
            else:
                msg_dict = dict(msg_row) if hasattr(msg_row, 'keys') else msg_row
            
            enriched_messages.append(msg_dict)
        
        return enriched_messages

    def can_access_chat(self, course_id, user_id, user_role):
        """Check if user can access course chat"""
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return False, "Course not found"
        
        # Teacher can always access
        if user_role == "teacher" and course.teacher_id == user_id:
            return True, "Access granted"
        
        # Student must be enrolled
        if user_role == "student":
            if self.enrollment_repo.is_enrolled(user_id, course_id):
                return True, "Access granted"
            else:
                return False, "You must be enrolled in this course"
        
        return False, "Unauthorized"

