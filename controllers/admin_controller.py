
from flask import Blueprint, render_template
from repositories.repository_factory import RepositoryFactory

admin_bp = Blueprint("admin", __name__)
user_repo_admin = RepositoryFactory.get("user")

@admin_bp.route("/users")
def users():
    users = user_repo_admin.get_all()
    return render_template("admin_users.html", users=users)
