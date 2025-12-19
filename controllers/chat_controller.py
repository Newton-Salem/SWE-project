from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.chat_service import ChatService
from services.course_service import CourseService

chat_bp = Blueprint("chat", __name__)
chat_service = ChatService()
course_service = CourseService()

def login_required(f):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@chat_bp.route("/course/<int:course_id>/chat", methods=["GET", "POST"])
@login_required
def course_chat(course_id):
    user_id = session["user_id"]
    user_role = session.get("role")
    
    # Check access
    can_access, message = chat_service.can_access_chat(course_id, user_id, user_role)
    if not can_access:
        flash(message, "danger")
        return redirect(url_for("course.teacher_dashboard" if user_role == "teacher" else "course.student_dashboard"))

    if request.method == "POST":
        message_text = request.form.get("message", "").strip()
        success, msg = chat_service.send_message(course_id, user_id, message_text)
        flash(msg, "success" if success else "danger")
        return redirect(url_for("chat.course_chat", course_id=course_id))

    course = course_service.course_repo.get_by_id(course_id)
    if not course:
        flash("Course not found", "danger")
        return redirect(url_for("course.teacher_dashboard" if user_role == "teacher" else "course.student_dashboard"))
    
    messages = chat_service.get_messages(course_id)
    return render_template("chat.html",
                           course=course,
                           messages=messages,
                           user_id=user_id)