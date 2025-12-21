from flask import Blueprint, send_file, flash, redirect, url_for, session
from services.lecture_service import LectureService
from services.course_service import CourseService
from services.chat_service import ChatService
from controllers.course_controller import login_required
import os

file_bp = Blueprint("file", __name__)
lecture_service = LectureService()
course_service = CourseService()
chat_service = ChatService()

@file_bp.route("/download/lecture/<int:lecture_id>")
@login_required()
def download_lecture(lecture_id):
    """Download a lecture file"""
    # Get lecture by ID
    lecture = lecture_service.get_lecture_by_id(lecture_id)
    
    if not lecture or not lecture.file_path:
        flash("Lecture file not found", "danger")
        return redirect(url_for("course.teacher_dashboard" if session.get("role") == "teacher" else "course.student_dashboard"))
    
    # Check access 
    course = course_service.get_course_by_id(lecture.course_id)
    if not course:
        flash("Course not found", "danger")
        return redirect(url_for("course.teacher_dashboard" if session.get("role") == "teacher" else "course.student_dashboard"))
    
    user_id = session.get("user_id")
    user_role = session.get("role")
    
    # Teacher owns the course or student is enrolled
    if user_role == "teacher" and course.teacher_id == user_id:
        pass  # Teacher has access
    elif user_role == "student":
        can_access, message = chat_service.can_access_chat(lecture.course_id, user_id, user_role)
        if not can_access:
            flash("You don't have access to this file", "danger")
            return redirect(url_for("course.student_dashboard"))
    else:
        flash("Unauthorized", "danger")
        return redirect(url_for("course.teacher_dashboard" if user_role == "teacher" else "course.student_dashboard"))
    
    if os.path.exists(lecture.file_path):
        return send_file(lecture.file_path, as_attachment=True)
    else:
        flash("File not found on server", "danger")
        return redirect(url_for("course.teacher_dashboard" if user_role == "teacher" else "course.student_dashboard"))

@file_bp.route("/download/submission/<int:submission_id>")
@login_required()
def download_submission(submission_id):
    """Download a submission file (teacher only)"""
    if session.get("role") != "teacher":
        flash("Unauthorized", "danger")
        return redirect(url_for("course.student_dashboard"))
    
    submission_repo = RepositoryFactory.get("submission")

    flash("Feature not fully implemented", "warning")
    return redirect(url_for("course.teacher_dashboard"))
