from flask import Blueprint, render_template, session, redirect, url_for
from controllers.course_controller import login_required
from services.notification_service import NotificationService

notification_bp = Blueprint("notification", __name__)
notification_service = NotificationService()


@notification_bp.route("/")
@login_required()
def notifications():
    user_id = session["user_id"]

    notifications = notification_service.get_notifications_for_user(user_id)

    return render_template(
        "notifications.html",
        notifications=notifications
    )
