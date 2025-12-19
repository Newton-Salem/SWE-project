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
