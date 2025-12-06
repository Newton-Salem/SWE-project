from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from DAO.assignment_dao import AssignmentDAO
from DAO.submission_dao import SubmissionDAO
from DAO.course_dao import CourseDAO
import os

assignment_bp = Blueprint("assignment", __name__)
assignment_dao = AssignmentDAO()
submission_dao = SubmissionDAO()
course_dao = CourseDAO()

@assignment_bp.route("/course/<int:course_id>/assignments")
def assignments_list(course_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    course = course_dao.get_course(course_id)
    assignments = assignment_dao.get_assignments_for_course(course_id)
    role = session.get("role")

    return render_template("assignments.html",
                           course=course,
                           assignments=assignments,
                           role=role)

@assignment_bp.route("/course/<int:course_id>/assignments/create", methods=["GET", "POST"])
def create_assignment(course_id):
    if "user_id" not in session or session.get("role") != "teacher":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]  # "YYYY-MM-DD"
        max_grade = request.form["max_grade"]

        assignment_dao.create_assignment(course_id, title, description, due_date, max_grade)
        flash("Assignment created", "success")
        return redirect(url_for("assignment.assignments_list", course_id=course_id))

    return render_template("create_assignment.html", course_id=course_id)

@assignment_bp.route("/assignment/<int:assignment_id>/submit", methods=["GET", "POST"])
def submit_assignment(assignment_id):
    if "user_id" not in session or session.get("role") != "student":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        file = request.files.get("file")
        file_path = None
        if file and file.filename:
            upload_folder = "static/submissions"
            os.makedirs(upload_folder, exist_ok=True)
            file_path = f"{upload_folder}/{file.filename}"
            file.save(file_path)

        student_id = session.get("user_id")
        submission_dao.submit_assignment(assignment_id, student_id, file_path)
        flash("Submission uploaded", "success")
        return redirect(url_for("auth.student_dashboard"))

    return render_template("submit_assignment.html", assignment_id=assignment_id)

@assignment_bp.route("/assignment/<int:assignment_id>/submissions")
def view_submissions(assignment_id):
    if "user_id" not in session or session.get("role") != "teacher":
        return redirect(url_for("auth.login"))

    submissions = submission_dao.get_submissions_for_assignment(assignment_id)
    return render_template("submissions_list.html",
                           submissions=submissions,
                           assignment_id=assignment_id)

@assignment_bp.route("/submission/<int:submission_id>/grade", methods=["GET", "POST"])
def grade_submission(submission_id):
    if "user_id" not in session or session.get("role") != "teacher":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        grade = request.form["grade"]
        feedback = request.form["feedback"]
        submission_dao.grade_submission(submission_id, grade, feedback)
        flash("Submission graded", "success")
        return redirect(request.referrer or url_for("auth.teacher_dashboard"))

    return render_template("grade_submission.html", submission_id=submission_id)