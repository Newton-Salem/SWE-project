from repositories.repository_factory import RepositoryFactory


class NotificationService:
    def __init__(self):
        self.notification_repo = RepositoryFactory.get("notification")

    def create_notification(self, user_id, message, notif_type, ref_id):
        self.notification_repo.create(
            user_id,
            message,
            notif_type,
            ref_id
        )

    def get_notifications_for_user(self, user_id):
        return self.notification_repo.get_by_user(user_id)
