
from database.db import MySQLConnection
from models.user import User

class UserDAO:
    def __init__(self):
        db = MySQLConnection()
        self.conn = db.get_connection()
        self.cursor = db.get_cursor()

    def get_user_by_email(self, email):
       query = "SELECT user_id, name, email, password, role FROM users WHERE email = ?"
       self.cursor.execute(query, (email,))
       return self.cursor.fetchone()


    def create_user(self, name, email, password, role="student"):
        query = """
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (name, email, password, role))
        self.conn.commit()


