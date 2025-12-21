from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from services.lecture_service import LectureService
from controllers.course_controller import login_required

lecture_bp = Blueprint("lecture", __name__)
lecture_service = LectureService()

@lecture_bp.route("/upload/<int:course_id>", methods=["GET", "POST"])
@login_required("teacher")
def upload_lecture(course_id):
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        video_link = request.form.get("video_link", "").strip()
        file = request.files.get("file")

        file_path = None
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        max_file_size = current_app.config.get("MAX_CONTENT_LENGTH", 10 * 1024 * 1024)
        
        if file and file.filename:
            # Save file using service
            file_path = lecture_service.save_uploaded_file(file, upload_folder)

        success, message = lecture_service.upload_lecture(
            course_id, title, file_path, video_link, upload_folder, max_file_size
        )
        flash(message, "success" if success else "danger")
        
        if success:
            return redirect(url_for("course.teacher_dashboard"))
        else:
            return render_template("lectures.html", course_id=course_id, error=message)

    return render_template("lectures.html", course_id=course_id)

@lecture_bp.route("/view/<int:course_id>")
@login_required()   # أي حد logged in
def view_lectures(course_id):
    lectures = lecture_service.get_lectures_by_course(course_id)
    return render_template(
        "view_lectures.html",
        lectures=lectures,
        course_id=course_id
    )

@lecture_bp.route("/delete/<int:lecture_id>")
@login_required("teacher")
def delete_lecture(lecture_id):
    success, message = lecture_service.delete_lecture(lecture_id)
    flash(message, "success" if success else "danger")
    return redirect(request.referrer or url_for("course.teacher_dashboard"))

@lecture_bp.route("/edit/<int:lecture_id>", methods=["GET", "POST"])
@login_required("teacher")
def edit_lecture(lecture_id):
    if request.method == "POST":
        title = request.form.get("title")
        video_link = request.form.get("video_link")

        success, message = lecture_service.edit_lecture(
            lecture_id, title, video_link
        )
        flash(message, "success" if success else "danger")
        return redirect(request.referrer)

    lecture = lecture_service.get_lecture_by_id(lecture_id)
    return render_template("edit_lecture.html", lecture=lecture)