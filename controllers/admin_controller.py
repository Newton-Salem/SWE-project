from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from services.user_service import UserService
from controllers.course_controller import login_required

admin_bp = Blueprint("admin", __name__)
user_service = UserService()

@admin_bp.route("/users")
@login_required("admin")
def users():
    users_list = user_service.get_all_users()
    return render_template("admin_users.html", users=users_list)

@admin_bp.route("/users/create", methods=["GET", "POST"])
@login_required("admin")
def create_user():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "student")
        
        success, message = user_service.create_user(name, email, password, role)
        flash(message, "success" if success else "danger")
        
        if success:
            return redirect(url_for("admin.users"))
    
    return render_template("admin_create_user.html")

@admin_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@login_required("admin")
def delete_user(user_id):
    success, message = user_service.delete_user(user_id, session["user_id"])
    flash(message, "success" if success else "danger")
    return redirect(url_for("admin.users"))
