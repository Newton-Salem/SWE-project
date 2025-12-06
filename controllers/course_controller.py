from flask import Blueprint, render_template, request, redirect, session, flash
from DAO.course_dao import CourseDAO

course_bp = Blueprint("course", __name__)
course_dao = CourseDAO()

@course_bp.route("/create_course", methods=["GET", "POST"])
def create_course():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        code = request.form["code"]

        teacher_id = session.get("user_id")

        course_dao.create_course(teacher_id, title, description, code)
        flash("Course created successfully!", "success")
        return redirect("/dashboard")

    return render_template("create_course.html")


@course_bp.route("/join_course", methods=["GET", "POST"])
def join_course():
    if request.method == "POST":
        code = request.form["code"]
        student_id = session.get("user_id")

        result = course_dao.join_course(student_id, code)

        if result == "joined":
            flash("Joined course successfully!", "success")
        elif result == "already":
            flash("You already joined this course!", "info")
        else:
            flash("Course code not found!", "danger")

        return redirect("/dashboard")

    return render_template("join_course.html")


@course_bp.route("/course/<int:course_id>")
def course_page(course_id):
    course = course_dao.get_course(course_id)
    return render_template("course.html", course=course)