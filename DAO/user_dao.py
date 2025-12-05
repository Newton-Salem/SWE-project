
from database.db import MySQLConnection
from models.user import User

class UserDAO:
    def __init__(self):
        db = MySQLConnection()
        self.conn = db.get_connection()
        self.cursor = db.get_cursor()

    def get_user_by_email(self, email):
        query = "SELECT * FROM user WHERE email = %s LIMIT 1"
        self.cursor.execute(query, (email,))
        row = self.cursor.fetchone()
        if row:
            return User(row["user_id"], row["name"], row["email"], row["password"], row["role"])
        return None

    def create_user(self, name, email, password, role="student"):
        query = "INSERT INTO user(name, email, password, role) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (name, email, password, role))
        self.conn.commit()
        return True

