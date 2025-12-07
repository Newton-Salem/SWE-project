from repositories.base_repository import BaseRepository
from models.user import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def get_by_email(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = self.cursor.fetchone()
        return User.from_row(self.cursor, row)

    def get_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = self.cursor.fetchone()
        return User.from_row(self.cursor, row)

    def create_user(self, name, email, password_hash, role):
        self.cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (name, email, password_hash, role))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        users = []
        for row in rows:
            users.append(User.from_row(self.cursor, row))
        return users
