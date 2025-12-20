from flask import Blueprint, render_template, redirect, url_for, flash, Response, request
from controllers.course_controller import login_required
from services.admin_service import AdminService

admin_bp = Blueprint("admin", __name__)
admin_service = AdminService()


# =========================
# ADMIN DASHBOARD
# =========================
@admin_bp.route("/dashboard")
@login_required("admin")
def dashboard():
    users, courses = admin_service.get_dashboard_data()
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
        success, msg = admin_service.create_teacher(
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("password")
        )
        flash(msg, "success" if success else "danger")
        if success:
            return redirect(url_for("admin.dashboard"))

    return render_template("admin_create_teacher.html")


# =========================
# DELETE USER
# =========================
@admin_bp.route("/delete-user/<int:user_id>")
@login_required("admin")
def delete_user(user_id):
    success, msg = admin_service.delete_user(user_id)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("admin.dashboard"))


# =========================
# DELETE COURSE
# =========================
@admin_bp.route("/delete-course/<int:course_id>")
@login_required("admin")
def delete_course(course_id):
    success, msg = admin_service.delete_course(course_id)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("admin.dashboard"))


# =========================
# EXPORT USERS
# =========================
@admin_bp.route("/export/users")
@login_required("admin")
def export_users():
    csv_data = admin_service.export_users_csv()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=users.csv"}
    )


# =========================
# EXPORT COURSES
# =========================
@admin_bp.route("/export/courses")
@login_required("admin")
def export_courses():
    csv_data = admin_service.export_courses_csv()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=courses.csv"}
    )


# =========================
# RESET PASSWORD
# =========================
@admin_bp.route("/reset-password/<int:user_id>")
@login_required("admin")
def reset_user_password(user_id):
    success, msg = admin_service.reset_user_password(user_id)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("admin.dashboard"))


# =========================
# EDIT USER
# =========================
@admin_bp.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
@login_required("admin")
def edit_user(user_id):
    if request.method == "POST":
        success, msg = admin_service.edit_user(
            user_id,
            request.form.get("name"),
            request.form.get("email")
        )
        flash(msg, "success" if success else "danger")
        if success:
            return redirect(url_for("admin.dashboard"))

    user = admin_service.get_user_by_id(user_id)
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin_edit_user.html", user=user)