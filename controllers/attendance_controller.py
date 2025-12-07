from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import date
from repositories.repository_factory import RepositoryFactory
from controllers.course_controller import login_required

attendance_bp = Blueprint("attendance", __name__)
attendance_repo = RepositoryFactory.get("attendance")

@attendance_bp.route("/record/<int:course_id>", methods=["GET", "POST"])
@login_required("teacher")
def record_attendance(course_id):
    if request.method == "POST":
        students = request.form.getlist("student_id")
        statuses = request.form.getlist("status")

        for sid, st in zip(students, statuses):
            attendance_repo.mark_attendance(course_id, int(sid), date.today(), st)

        flash("Attendance saved", "success")
        return redirect(url_for("course.teacher_dashboard"))

    students = attendance_repo.get_students_in_course(course_id)
    return render_template("attendance.html", course_id=course_id, students=students)
