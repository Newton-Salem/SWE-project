from repositories.repository_factory import RepositoryFactory


class NotificationService:
    def __init__(self):
        self.notification_repo = RepositoryFactory.get("notification")

    # CREATE NOTIFICATION

    def create_notification(self, user_id, message, notification_type, reference_id=None):
        if not user_id:
            return False, "Invalid user"

        if not message or not message.strip():
            return False, "Empty message"

        self.notification_repo.create(
            user_id=user_id,
            message=message.strip(),
            notif_type=notification_type,
            ref_id=reference_id
        )

        return True, "Notification created"

<<<<<<< HEAD
    # ==================================================
    # GET USER NOTIFICATIONS
    # ==================================================
=======
    # GET USER NOTIFICATIONS

>>>>>>> afe8f5132ed2cacb0ca1acde2f713dc889375586
    def get_user_notifications(self, user_id):
        if not user_id:
            return []

        return self.notification_repo.get_by_user(user_id)

<<<<<<< HEAD
    # ==================================================
    # DELETE ALL USER NOTIFICATIONS
    # ==================================================
=======
    # DELETE ALL USER NOTIFICATIONS
    
>>>>>>> afe8f5132ed2cacb0ca1acde2f713dc889375586
    def delete_user_notifications(self, user_id):
        if not user_id:
            return False

        self.notification_repo.delete_by_user(user_id)
        return True