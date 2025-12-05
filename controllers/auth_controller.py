
from flask import Blueprint, render_template, request, redirect, session
from DAO.user_dao import UserDAO
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

user_dao = UserDAO()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = user_dao.get_user_by_email(email)

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.user_id
            session["role"] = user.role

            if user.role == "teacher":
                return redirect("/teacher/dashboard")
            elif user.role == "student":
                return redirect("/student/dashboard")
            elif user.role == "admin":
                return redirect("/admin/panel")

        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        user_dao.create_user(name, email, password)
        return redirect("/login")

    return render_template("register.html")

