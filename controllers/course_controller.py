
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from services.course_service import CourseService

course_bp = Blueprint("course", __name__)
course_service = CourseService()

def login_required(role=None):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("auth.login"))
            if role and session.get("role") != role:
                flash("Unauthorized", "danger")
                return redirect(url_for("auth.login"))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

@course_bp.route("/teacher")
@login_required("teacher")
def teacher_dashboard():
    courses = course_service.get_teacher_courses(session["user_id"])
    return render_template("dashboard_teacher.html", courses=courses)

@course_bp.route("/student")
@login_required("student")
def student_dashboard():
    courses = course_service.get_student_courses(session["user_id"])
    return render_template("dashboard_student.html", courses=courses)

@course_bp.route("/create", methods=["GET", "POST"])
@login_required("teacher")
def create_course():
    if request.method == "POST":
        title = request.form["title"]
        code = request.form["code"]
        description = request.form["description"]
        course_service.create_course(session["user_id"], title, code, description)
        flash("Course created", "success")
        return redirect(url_for("course.teacher_dashboard"))

    return render_template("course.html", mode="create")

@course_bp.route("/join", methods=["GET", "POST"])
@login_required("student")
def join_course():
    if request.method == "POST":
        code = request.form["code"]
        ok, msg = course_service.join_course(session["user_id"], code)
        flash(msg, "success" if ok else "danger")
        if ok:
            return redirect(url_for("course.student_dashboard"))
        return render_template("course.html", mode="join")

    return render_template("course.html", mode="join")
