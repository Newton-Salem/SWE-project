from flask import Blueprint, render_template, request, redirect, url_for, session
from DAO.chat_dao import ChatDAO
from DAO.course_dao import CourseDAO

chat_bp = Blueprint("chat", __name__)
chat_dao = ChatDAO()
course_dao = CourseDAO()

@chat_bp.route("/course/<int:course_id>/chat", methods=["GET", "POST"])
def course_chat(course_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        message = request.form["message"].strip()
        if message:
            chat_dao.add_message(course_id, session["user_id"], message)
        return redirect(url_for("chat.course_chat", course_id=course_id))

    course = course_dao.get_course(course_id)
    messages = chat_dao.get_messages(course_id)
    return render_template("chat.html",
                           course=course,
                           messages=messages)