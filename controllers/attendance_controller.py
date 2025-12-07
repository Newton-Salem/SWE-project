from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from DAO.attendance_dao import AttendanceDAO
from DAO.course_dao import CourseDAO
from database.db import MySQLConnection

attendance_bp = Blueprint("attendance", __name__)
attendance_dao = AttendanceDAO()
course_dao = CourseDAO()

@attendance_bp.route("/course/<int:course_id>/attendance", methods=["GET", "POST"])
def course_attendance(course_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    role = session.get("role")
    course = course_dao.get_course(course_id)

    db = MySQLConnection()
    cursor = db.get_cursor()

   
    cursor.execute("""
        SELECT u.user_id, u.name
        FROM enrollment e
        JOIN users u ON e.student_id = u.user_id
        WHERE e.course_id=%s
    """, (course_id,))
    students = cursor.fetchall()

    if request.method == "POST" and role == "teacher":
        for s in students:
            status = request.form.get(f"status_{s['user_id']}")
            if status:
                attendance_dao.mark_attendance(course_id, s["user_id"], status)
        flash("Attendance saved", "success")
        return redirect(url_for("attendance.course_attendance", course_id=course_id))

    records = attendance_dao.get_attendance_for_course(course_id)

    return render_template("attendance.html",
                           course=course,
                           students=students,
                           records=records,
                           role=role)