from werkzeug.security import generate_password_hash
from repositories.repository_factory import RepositoryFactory


class AdminService:
    def __init__(self):
        self.user_repo = RepositoryFactory.get("user")

    def create_teacher(self, name, email, password):
        if self.user_repo.get_by_email(email):
            return False, "Email already exists"

        hashed = generate_password_hash(password)
        self.user_repo.create_user(
            name=name,
            email=email,
            password_hash=hashed,
            role="teacher"
        )
        return True, "Teacher created successfully"