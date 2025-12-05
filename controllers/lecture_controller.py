from flask import Blueprint, render_template, request, redirect, flash
from DAO.lecture_dao import LectureDAO

lecture_bp = Blueprint("lecture", __name__)
lecture_dao = LectureDAO()

@lecture_bp.route("/course/<int:course_id>/lectures")
def view_lectures(course_id):
    lectures = lecture_dao.get_lectures(course_id)
    return render_template("lectures.html", lectures=lectures, course_id=course_id)


@lecture_bp.route("/course/<int:course_id>/upload", methods=["GET", "POST"])
def upload_lecture(course_id):
    if request.method == "POST":
        title = request.form["title"]
        video_link = request.form.get("video_link")
        file = request.files.get("file")

        file_path = None
        if file:
            file_path = f"uploads/{file.filename}"
            file.save(file_path)

        lecture_dao.add_lecture(course_id, title, file_path, video_link)
        flash("Lecture uploaded!", "success")

        return redirect(f"/course/{course_id}/lectures")

    return render_template("upload_lecture.html", course_id=course_id)