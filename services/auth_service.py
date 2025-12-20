from werkzeug.security import generate_password_hash, check_password_hash
from repositories.repository_factory import RepositoryFactory
from datetime import datetime, timedelta
import uuid


class AuthService:
    def __init__(self):
        self.user_repo = RepositoryFactory.get("user")

    # =========================
    # REGISTER
    # =========================
    def register_user(self, name, email, password, role):
        existing = self.user_repo.get_by_email(email)
        if existing:
            return False, "Email already registered"

        hashed = generate_password_hash(password)
        self.user_repo.create_user(name, email, hashed, role)
        return True, "Registered successfully"

    # =========================
    # LOGIN  ✅ دي كانت المشكلة
    # =========================
    def authenticate(self, email, password):
        user = self.user_repo.get_by_email(email)
        if not user:
            return None

        if not check_password_hash(user.password, password):
            return None

        return user

    # =========================
    # FORGOT PASSWORD
    # =========================
    def forgot_password(self, email):
        user = self.user_repo.get_by_email(email)
        if not user:
            return False, "Email not found"

        token = str(uuid.uuid4())
        expiry = datetime.now() + timedelta(minutes=30)

        self.user_repo.set_reset_token(email, token, expiry)

        # مؤقتًا في الكونسول
        reset_link = f"http://127.0.0.1:5000/auth/reset-password/{token}"
        print("RESET PASSWORD LINK:", reset_link)

        return True, "Reset link sent (check console)"

    # =========================
    # RESET PASSWORD
    # =========================
    def reset_password(self, token, new_password):
        user = self.user_repo.get_by_reset_token(token)
        if not user:
            return False, "Invalid or expired link"

        hashed = generate_password_hash(new_password)
        self.user_repo.update_password(user.user_id, hashed)

        return True, "Password updated successfully"
