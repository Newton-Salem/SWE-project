from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.attendance_service import AttendanceService
from controllers.course_controller import login_required

attendance_bp = Blueprint("attendance", __name__)
attendance_service = AttendanceService()

@attendance_bp.route("/record/<int:course_id>", methods=["GET", "POST"])
@login_required("teacher")
def record_attendance(course_id):
    if request.method == "POST":
        # Get all form fields that start with "status_"
        attendance_data = {}
        for key, value in request.form.items():
            if key.startswith("status_"):
                student_id = key.replace("status_", "")
                if value:  # Only add if status is selected
                    attendance_data[student_id] = value

        success, message = attendance_service.record_attendance(
            course_id, attendance_data
        )
        flash(message, "success" if success else "danger")
        
        if success:
            return redirect(url_for("course.teacher_dashboard"))
        else:
            students = attendance_service.get_students_for_attendance(course_id)
            return render_template("attendance.html", course_id=course_id, students=students, error=message)

    students = attendance_service.get_students_for_attendance(course_id)
    if not students:
        flash("No students enrolled in this course", "warning")
        return redirect(url_for("course.teacher_dashboard"))
    
    return render_template("attendance.html", course_id=course_id, students=students)
