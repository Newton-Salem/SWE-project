
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from repositories.repository_factory import RepositoryFactory
from datetime import date
import os
from controllers.course_controller import login_required

lecture_bp = Blueprint("lecture", __name__)
lecture_repo = RepositoryFactory.get("lecture")

@lecture_bp.route("/upload/<int:course_id>", methods=["GET", "POST"])
@login_required("teacher")
def upload_lecture(course_id):
    if request.method == "POST":
        title = request.form["title"]
        video_link = request.form.get("video_link", "")
        file = request.files.get("file")

        file_path = None
        if file and file.filename:
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, file.filename)
            file.save(file_path)

        lecture_repo.add_lecture(course_id, title, file_path, video_link, date.today())
        flash("Lecture uploaded", "success")
        return redirect(url_for("course.teacher_dashboard"))

    return render_template("lectures.html", course_id=course_id)
