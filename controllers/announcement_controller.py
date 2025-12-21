from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from services.announcement_service import AnnouncementService
from controllers.course_controller import login_required

announcement_bp = Blueprint("announcement", __name__)
announcement_service = AnnouncementService()


@announcement_bp.route("/create/<int:course_id>", methods=["GET", "POST"])
@login_required("teacher")
def create_announcement(course_id):
    """
    Controller:
    - handles request/session/render
    - delegates logic to service
    """
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")

        success, message = announcement_service.create_announcement(
            course_id=course_id,
            teacher_id=session["user_id"],
            title=title,
            content=content
        )

        flash(message, "success" if success else "danger")

        if success:
            return redirect(url_for("announcement.view_announcements", course_id=course_id))

    # GET request OR failed POST
    course = announcement_service.get_course_for_teacher(
        course_id=course_id,
        teacher_id=session["user_id"]
    )

    if not course:
        flash("Unauthorized or course not found", "danger")
        return redirect(url_for("course.teacher_dashboard"))

    return render_template("create_announcement.html", course=course)


@announcement_bp.route("/view/<int:course_id>")
@login_required()
def view_announcements(course_id):
    """
    Controller:
    - just fetch & render
    """
    course, announcements = announcement_service.get_course_announcements(course_id)

    if not course:
        flash("Course not found", "danger")
        dashboard = (
            "course.teacher_dashboard"
            if session.get("role") == "teacher"
            else "course.student_dashboard"
        )
        return redirect(url_for(dashboard))

    return render_template(
        "announcements.html",
        course=course,
        announcements=announcements
    )
