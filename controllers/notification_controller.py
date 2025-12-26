from flask import Blueprint, render_template, session, redirect, url_for, flash
from controllers.course_controller import login_required
from services.notification_service import NotificationService

notification_bp = Blueprint("notification", __name__)
notification_service = NotificationService()


@notification_bp.route("/")
@login_required()
def notifications():
    """
    Controller:
    - handles session & rendering
    - delegates logic to service
    """
    user_id = session.get("user_id")

    if not user_id:
        flash("Unauthorized access", "danger")
        return redirect(url_for("auth.login"))

    notifications = notification_service.get_user_notifications(user_id)

    return render_template(
        "notifications.html",
        notifications=notifications
    )