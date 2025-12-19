from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from services.assignment_service import AssignmentService
from services.submission_service import SubmissionService
import os
from controllers.course_controller import login_required

assignment_bp = Blueprint("assignment", __name__)
assignment_service = AssignmentService()
submission_service = SubmissionService()

@assignment_bp.route("/create/<int:course_id>", methods=["GET", "POST"])
@login_required("teacher")
def create_assignment(course_id):
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        due_date = request.form.get("due_date", "")
        max_grade = request.form.get("max_grade", "")

        success, message = assignment_service.create_assignment(
            course_id, title, description, due_date, max_grade
        )
        flash(message, "success" if success else "danger")
        
        if success:
            return redirect(url_for("course.teacher_dashboard"))
        else:
            return render_template("assignments.html", course_id=course_id, error=message)

    return render_template("assignments.html", course_id=course_id)

@assignment_bp.route("/submit/<int:assignment_id>", methods=["GET", "POST"])
@login_required("student")
def submit_assignment(assignment_id):
    assignment = assignment_service.get_assignment_by_id(assignment_id)
    if not assignment:
        flash("Assignment not found", "danger")
        return redirect(url_for("course.student_dashboard"))
    
    # Check if can submit
    can_submit, message = submission_service.can_submit(assignment_id, session["user_id"])
    if not can_submit:
        flash(message, "danger")
        return redirect(url_for("course.student_dashboard"))
    
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename:
            flash("Please choose a file", "danger")
            return redirect(request.url)

        # Check file size (10MB limit)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        if file_size > current_app.config.get("MAX_CONTENT_LENGTH", 10 * 1024 * 1024):
            flash("File size exceeds 10MB limit", "danger")
            return redirect(request.url)

        # Save file
        from services.lecture_service import LectureService
        lecture_service = LectureService()
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        file_path = lecture_service.save_uploaded_file(file, upload_folder)

        # Submit assignment
        success, message = assignment_service.submit_assignment(
            assignment_id, session["user_id"], file_path
        )
        flash(message, "success" if success else "danger")
        
        if success:
            return redirect(url_for("course.student_dashboard"))
        else:
            return render_template("submit_assignment.html", assignment=assignment, error=message)

    return render_template("submit_assignment.html", assignment=assignment)

@assignment_bp.route("/view/<int:course_id>")
@login_required()
def view_assignments(course_id):
    """View all assignments for a course"""
    from services.course_service import CourseService
    course_service = CourseService()
    
    assignments = assignment_service.get_assignments_by_course(course_id)
    course = course_service.course_repo.get_by_id(course_id)
    return render_template("assignments.html", assignments=assignments, course=course)

@assignment_bp.route("/submissions/<int:assignment_id>")
@login_required("teacher")
def view_submissions(assignment_id):
    """View all submissions for an assignment"""
    assignment = assignment_service.get_assignment_by_id(assignment_id)
    if not assignment:
        flash("Assignment not found", "danger")
        return redirect(url_for("course.teacher_dashboard"))
    
    submissions = assignment_service.get_submissions_by_assignment(assignment_id)
    return render_template("submission_list.html", submissions=submissions, assignment=assignment)

@assignment_bp.route("/grade/<int:submission_id>", methods=["GET", "POST"])
@login_required("teacher")
def grade_submission(submission_id):
    """Grade a submission"""
    submission_details = submission_service.get_submission_with_details(submission_id)
    if not submission_details:
        flash("Submission not found", "danger")
        return redirect(url_for("course.teacher_dashboard"))
    
    submission = submission_details['submission']
    student = submission_details['student']
    assignment = submission_details['assignment']
    
    if request.method == "POST":
        grade = request.form.get("grade", "").strip()
        feedback = request.form.get("feedback", "").strip()
        
        success, message = assignment_service.grade_submission(
            submission_id, grade, feedback, session["user_id"]
        )
        flash(message, "success" if success else "danger")
        
        if success:
            return redirect(url_for("assignment.view_submissions", assignment_id=submission.assignment_id))
        else:
            return render_template("grade_submission.html", 
                                 submission=submission, 
                                 student=student,
                                 assignment=assignment,
                                 error=message)
    
    return render_template("grade_submission.html", 
                         submission=submission, 
                         student=student,
                         assignment=assignment)
