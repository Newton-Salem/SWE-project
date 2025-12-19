from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from services.announcement_service import AnnouncementService
from services.course_service import CourseService
from controllers.course_controller import login_required

announcement_bp = Blueprint("announcement", __name__)
announcement_service = AnnouncementService()
course_service = CourseService()

@announcement_bp.route("/create/<int:course_id>", methods=["GET", "POST"])
@login_required("teacher")
def create_announcement(course_id):
    """Create a new announcement"""
    course = course_service.course_repo.get_by_id(course_id)
    if not course:
        flash("Course not found", "danger")
        return redirect(url_for("course.teacher_dashboard"))
    
    if course.teacher_id != session["user_id"]:
        flash("Unauthorized: You don't own this course", "danger")
        return redirect(url_for("course.teacher_dashboard"))
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        
        success, message = announcement_service.create_announcement(
            course_id, session["user_id"], title, content
        )
        flash(message, "success" if success else "danger")
        
        if success:
            return redirect(url_for("announcement.view_announcements", course_id=course_id))
        else:
            return render_template("create_announcement.html", course=course, error=message)
    
    return render_template("create_announcement.html", course=course)

@announcement_bp.route("/view/<int:course_id>")
@login_required()
def view_announcements(course_id):
    """View all announcements for a course"""
    course = course_service.course_repo.get_by_id(course_id)
    if not course:
        flash("Course not found", "danger")
        return redirect(url_for("course.teacher_dashboard" if session.get("role") == "teacher" else "course.student_dashboard"))
    
    announcements = announcement_service.get_announcements_by_course(course_id)
    return render_template("announcements.html", announcements=announcements, course=course)

