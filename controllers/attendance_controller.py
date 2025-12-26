from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from services.attendance_service import AttendanceService
from controllers.course_controller import login_required

attendance_bp = Blueprint("attendance", __name__)
attendance_service = AttendanceService()

@attendance_bp.route("/record/<int:course_id>", methods=["GET", "POST"])
@login_required("teacher")
def record_attendance(course_id):
    if request.method == "POST":
        attendance_data = {}

        for key, value in request.form.items():
            if key.startswith("status_"):
                student_id = key.replace("status_", "")
                attendance_data[student_id] = value

        success, message = attendance_service.record_attendance(
            course_id,
            attendance_data
        )

        flash(message, "success" if success else "danger")
        return redirect(url_for("course.teacher_dashboard"))

    students = attendance_service.get_students_for_attendance(course_id)
    return render_template("attendance.html", course_id=course_id, students=students)


@attendance_bp.route("/student/<int:course_id>")
@login_required("student")
def student_attendance(course_id):
    records = attendance_service.get_attendance_for_student(
        course_id,
        session["user_id"]
    )

    return render_template(
        "student_attendance.html",
        records=records,
        course_id=course_id
    )
