from flask import Blueprint, render_template, redirect, url_for, flash, Response, request
from controllers.course_controller import login_required
from repositories.repository_factory import RepositoryFactory
from services.admin_service import AdminService
from werkzeug.security import generate_password_hash
import csv

admin_bp = Blueprint("admin", __name__)

user_repo = RepositoryFactory.get("user")
course_repo = RepositoryFactory.get("course")
admin_service = AdminService()

# =========================
# ADMIN DASHBOARD
# =========================
@admin_bp.route("/dashboard")
@login_required("admin")
def dashboard():
    users = user_repo.get_all()
    courses = course_repo.get_all()
    return render_template(
        "dashboard_admin.html",
        users=users,
        courses=courses
    )

# =========================
# CREATE TEACHER
# =========================
@admin_bp.route("/create-teacher", methods=["GET", "POST"])
@login_required("admin")
def create_teacher():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        success, msg = admin_service.create_teacher(name, email, password)
        flash(msg, "success" if success else "danger")

        if success:
            return redirect(url_for("admin.dashboard"))

    return render_template("admin_create_teacher.html")

# =========================
# DELETE USER (SAFE)
# =========================
@admin_bp.route("/delete-user/<int:user_id>")
@login_required("admin")
def delete_user(user_id):
    user = user_repo.get_by_id(user_id)
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("admin.dashboard"))

    # ❗ امسحي Notifications الأول
    notif_repo = RepositoryFactory.get("notification")
    notif_repo.delete_by_user(user_id)

    user_repo.delete(user_id)
    flash("User deleted successfully", "success")
    return redirect(url_for("admin.dashboard"))

# =========================
# DELETE COURSE
# =========================
@admin_bp.route("/delete-course/<int:course_id>")
@login_required("admin")
def delete_course(course_id):
    course_repo.delete(course_id)
    flash("Course deleted successfully", "success")
    return redirect(url_for("admin.dashboard"))

# =========================
# EXPORT USERS (CSV)
# =========================
@admin_bp.route("/export/users")
@login_required("admin")
def export_users():
    users = user_repo.get_all()

    def generate():
        yield "ID,Name,Email,Role\n"
        for u in users:
            yield f"{u.user_id},{u.name},{u.email},{u.role}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=users.csv"}
    )

# =========================
# EXPORT COURSES (CSV)
# =========================
@admin_bp.route("/export/courses")
@login_required("admin")
def export_courses():
    courses = course_repo.get_all()

    def generate():
        yield "ID,Title,Code,TeacherID\n"
        for c in courses:
            yield f"{c.course_id},{c.title},{c.code},{c.teacher_id}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=courses.csv"}
    )

# =========================
# RESET USER PASSWORD
# =========================
@admin_bp.route("/reset-password/<int:user_id>")
@login_required("admin")
def reset_user_password(user_id):
    temp_password = "Reset@123"
    hashed = generate_password_hash(temp_password)
    user_repo.update_password(user_id, hashed)

    flash("Password reset to Reset@123", "success")
    return redirect(url_for("admin.dashboard"))

# =========================
@admin_bp.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
@login_required("admin")
def edit_user(user_id):
    user = user_repo.get_by_id(user_id)
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            flash("Name and Email are required", "danger")
            return redirect(request.url)

        user_repo.update_user(user_id, name, email)
        flash("User updated successfully", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin_edit_user.html",
        user=user
    )

