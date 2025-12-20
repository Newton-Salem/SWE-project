from repositories.repository_factory import RepositoryFactory
from werkzeug.security import generate_password_hash


class AdminService:
    def __init__(self):
        self.user_repo = RepositoryFactory.get("user")
        self.course_repo = RepositoryFactory.get("course")
        self.notification_repo = RepositoryFactory.get("notification")

    # =========================
    def get_dashboard_data(self):
        return self.user_repo.get_all(), self.course_repo.get_all()

    # =========================
    def create_teacher(self, name, email, password):
        if not name or not email or not password:
            return False, "All fields are required"

        if self.user_repo.get_by_email(email):
            return False, "Email already exists"

        hashed = generate_password_hash(password)
        self.user_repo.create_user(name.strip(), email.strip(), hashed, "teacher")
        return True, "Teacher created successfully"

    # =========================
    def delete_user(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found"

        self.notification_repo.delete_by_user(user_id)
        self.user_repo.delete(user_id)
        return True, "User deleted successfully"

    # =========================
    def delete_course(self, course_id):
        if not self.course_repo.get_by_id(course_id):
            return False, "Course not found"

        self.course_repo.delete(course_id)
        return True, "Course deleted successfully"

    # =========================
    def export_users_csv(self):
        users = self.user_repo.get_all()
        lines = ["ID,Name,Email,Role\n"]
        for u in users:
            lines.append(f"{u.user_id},{u.name},{u.email},{u.role}\n")
        return "".join(lines)

    # =========================
    def export_courses_csv(self):
        courses = self.course_repo.get_all()
        lines = ["ID,Title,Code,TeacherID\n"]
        for c in courses:
            lines.append(f"{c.course_id},{c.title},{c.code},{c.teacher_id}\n")
        return "".join(lines)

    # =========================
    def reset_user_password(self, user_id, temp="Reset@123"):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found"

        hashed = generate_password_hash(temp)
        self.user_repo.update_password(user_id, hashed)
        return True, f"Password reset to {temp}"

    # =========================
    def edit_user(self, user_id, name, email):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found"

        if not name or not email:
            return False, "Name and email are required"

        existing = self.user_repo.get_by_email(email)
        if existing and existing.user_id != user_id:
            return False, "Email already taken"

        self.user_repo.update_user(user_id, name.strip(), email.strip())
        return True, "User updated successfully"

    # =========================
    def get_user_by_id(self, user_id):
        return self.user_repo.get_by_id(user_id)