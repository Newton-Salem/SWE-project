from werkzeug.security import generate_password_hash, check_password_hash
from repositories.repository_factory import RepositoryFactory

class AuthService:
    def __init__(self):
        self.user_repo = RepositoryFactory.get("user")

    def register_user(self, name, email, password, role):
        existing = self.user_repo.get_by_email(email)
        if existing:
            return False, "Email already registered"
        hashed = generate_password_hash(password)
        self.user_repo.create_user(name, email, hashed, role)
        return True, "Registered successfully"

    def authenticate(self, email, password):
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        if not check_password_hash(user.password, password):
            return None
        return user
