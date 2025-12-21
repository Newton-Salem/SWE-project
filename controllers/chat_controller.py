from flask import Blueprint, render_template, request, redirect, session
from services.chat_service import ChatService
from controllers.course_controller import login_required

chat_bp = Blueprint("chat", __name__)
chat_service = ChatService()

# For STUDENT 
@chat_bp.route("/course/<int:course_id>/chat", methods=["GET", "POST"])
@login_required("student")
def student_chat(course_id):
    student_id = session["user_id"]

    if request.method == "POST":
        chat_service.send_message(
            course_id,
            student_id,   
            student_id,   
            request.form["message"]
        )
        return redirect(request.url)

    messages = chat_service.get_student_chat(course_id, student_id)
    return render_template("chat.html", messages=messages)


# For TEACHER 
@chat_bp.route("/course/<int:course_id>/teacher")
@login_required("teacher")
def teacher_students(course_id):
    students = chat_service.get_students_with_chats(course_id)
    return render_template(
        "chat_students.html",
        students=students,
        course_id=course_id
    )

@chat_bp.route("/course/<int:course_id>/chat/<int:student_id>", methods=["GET", "POST"])
@login_required("teacher")
def teacher_chat(course_id, student_id):
    teacher_id = session["user_id"]

    if request.method == "POST":
        chat_service.send_message(
            course_id,
            student_id,   # الشات تابع للطالب
            teacher_id,   # sender = المدرس
            request.form["message"]
        )
        return redirect(request.url)

    messages = chat_service.get_student_chat(course_id, student_id)
    return render_template("chat.html", messages=messages)