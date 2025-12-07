from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        ok, msg = auth_service.register_user(name, email, password, role)
        flash(msg, "success" if ok else "danger")
        if ok:
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = auth_service.authenticate(email, password)
        if not user:
            flash("Invalid email or password", "danger")
            return render_template("auth/login.html")

        session["user_id"] = user.user_id
        session["role"] = user.role

        if user.role == "teacher":
            return redirect(url_for("course.teacher_dashboard"))
        elif user.role == "student":
            return redirect(url_for("course.student_dashboard"))
        else:
            return redirect(url_for("admin.users"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


