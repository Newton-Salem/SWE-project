from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from repositories.repository_factory import RepositoryFactory
import os
from controllers.course_controller import login_required

assignment_bp = Blueprint("assignment", __name__)
assignment_repo = RepositoryFactory.get("assignment")
submission_repo = RepositoryFactory.get("submission")

@assignment_bp.route("/create/<int:course_id>", methods=["GET", "POST"])
@login_required("teacher")
def create_assignment(course_id):
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        max_grade = request.form["max_grade"]

        assignment_repo.create_assignment(course_id, title, description, due_date, max_grade)
        flash("Assignment created", "success")
        return redirect(url_for("course.teacher_dashboard"))

    return render_template("assignments.html", course_id=course_id)

@assignment_bp.route("/submit/<int:assignment_id>", methods=["GET", "POST"])
@login_required("student")
def submit_assignment(assignment_id):
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename:
            flash("Please choose a file", "danger")
            return redirect(request.url)

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)
        path = os.path.join(upload_folder, file.filename)
        file.save(path)

        submission_repo.submit(assignment_id, session["user_id"], path)
        flash("Assignment submitted", "success")
        return redirect(url_for("course.student_dashboard"))

    return render_template("submit_assignment.html", assignment_id=assignment_id)
