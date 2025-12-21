from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for,
    session, current_app
)

from services.assignment_service import AssignmentService
from services.submission_service import SubmissionService
from services.lecture_service import LectureService
from controllers.course_controller import login_required

assignment_bp = Blueprint("assignment", __name__)

assignment_service = AssignmentService()
submission_service = SubmissionService()
lecture_service = LectureService()


# TEACHER ROUTES


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

    return render_template("assignments.html", course_id=course_id)


@assignment_bp.route("/submissions/<int:assignment_id>")
@login_required("teacher")
def view_submissions(assignment_id):
    assignment = assignment_service.get_assignment_by_id(assignment_id)
    if not assignment:
        flash("Assignment not found", "danger")
        return redirect(url_for("course.teacher_dashboard"))

    submissions = assignment_service.get_submissions_by_assignment(assignment_id)

    return render_template(
        "submission_list.html",
        submissions=submissions,
        assignment=assignment
    )


@assignment_bp.route("/grade/<int:submission_id>", methods=["GET", "POST"])
@login_required("teacher")
def grade_submission(submission_id):
    details = submission_service.get_submission_with_details(submission_id)
    if not details:
        flash("Submission not found", "danger")
        return redirect(url_for("course.teacher_dashboard"))

    submission = details["submission"]
    student = details["student"]
    assignment = details["assignment"]

    if request.method == "POST":
        grade = request.form.get("grade", "").strip()
        feedback = request.form.get("feedback", "").strip()

        success, message = assignment_service.grade_submission(
            submission_id,
            session["user_id"],  # teacher_id
            grade,
            feedback
        )

        flash(message, "success" if success else "danger")
        if success:
            return redirect(
                url_for(
                    "assignment.view_submissions",
                    assignment_id=submission.assignment_id
                )
            )

    return render_template(
        "grade_submission.html",
        submission=submission,
        student=student,
        assignment=assignment
    )


@assignment_bp.route("/delete/<int:assignment_id>", methods=["POST"])
@login_required("teacher")
def delete_assignment(assignment_id):
    success, message = assignment_service.delete_assignment(
        assignment_id,
        session["user_id"]
    )

    flash(message, "success" if success else "danger")
    return redirect(url_for("course.teacher_dashboard"))



# STUDENT ROUTES 


@assignment_bp.route("/submit/<int:assignment_id>", methods=["GET", "POST"])
@login_required("student")
def submit_assignment(assignment_id):
    assignment = assignment_service.get_assignment_by_id(assignment_id)
    if not assignment:
        flash("Assignment not found", "danger")
        return redirect(url_for("course.student_dashboard"))

    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename:
            flash("File is required", "danger")
            return redirect(request.url)

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        file_path = lecture_service.save_uploaded_file(file, upload_folder)

        success, message = assignment_service.submit_assignment(
            assignment_id,
            session["user_id"],
            file_path
        )

        flash(message, "success" if success else "danger")
        return redirect(url_for("course.student_dashboard"))

    return render_template(
        "submit_assignment.html",
        assignment=assignment
    )


@assignment_bp.route("/status/<int:assignment_id>")
@login_required("student")
def assignment_status(assignment_id):
    student_id = session["user_id"]

    data = assignment_service.get_student_assignment_status(
        assignment_id,
        student_id
    )

    if not data:
        flash("Assignment not found", "danger")
        return redirect(url_for("course.student_dashboard"))

    return render_template(
        "assignment_status.html",
        assignment=data["assignment"],
        submission=data["submission"]
    )



#  SHARED VIEW (STUDENT and TEACHER) 


@assignment_bp.route("/view/<int:course_id>")
@login_required()
def view_assignments(course_id):
    role = session.get("role")
    student_id = session["user_id"] if role == "student" else None

    assignments = assignment_service.get_assignments_by_course(
        course_id,
        student_id
    )

    return render_template(
        "view_assignments.html",
        assignments=assignments,
        course_id=course_id,
        role=role
    )
