from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()


# REGISTER

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        role = "student"   

        ok, msg = auth_service.register_user(name, email, password, role)
        flash(msg, "success" if ok else "danger")
        if ok:
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html")



# LOGIN

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
        if user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        elif user.role == "student":
            return redirect(url_for("course.student_dashboard"))

    return render_template("auth/login.html")



# FORGOT PASSWORD

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        success, msg = auth_service.forgot_password(email)
        flash(msg, "success" if success else "danger")

    return render_template("auth/forgot_password.html")



# RESET PASSWORD

@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if request.method == "POST":
        password = request.form["password"]
        success, msg = auth_service.reset_password(token, password)
        flash(msg, "success" if success else "danger")
        if success:
            return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html")



# LOGOUT

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))