from repositories.base_repository import BaseRepository
from models.user import User


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__()


    # GET METHODS
    
    def get_by_email(self, email):
        self.cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )
        row = self.cursor.fetchone()
        return User.from_row(self.cursor, row) if row else None

    def get_by_id(self, user_id):
        self.cursor.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = self.cursor.fetchone()
        return User.from_row(self.cursor, row) if row else None

    def get_all(self):
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        return [User.from_row(self.cursor, row) for row in rows]

    
    # CREATE
   
    def create_user(self, name, email, password_hash, role):
        self.cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (name, email, password_hash, role))
        self.conn.commit()


    #  FORGOT PASSWORD
   
    def set_reset_token(self, user_id, token, expiry):
        self.cursor.execute("""
            UPDATE users
            SET reset_token = ?, reset_token_expiry = ?
            WHERE user_id = ?
        """, (token, expiry, user_id))
        self.conn.commit()

    def get_by_reset_token(self, token):
        self.cursor.execute("""
            SELECT *
            FROM users
            WHERE reset_token = ?
              AND reset_token_expiry > GETDATE()
        """, (token,))
        row = self.cursor.fetchone()
        return User.from_row(self.cursor, row) if row else None

    def update_password(self, user_id, hashed_password):
        self.cursor.execute("""
            UPDATE users
            SET password = ?, reset_token = NULL, reset_token_expiry = NULL
            WHERE user_id = ?
        """, (hashed_password, user_id))
        self.conn.commit()

    
    #  DELETE USER 
   
    def delete(self, user_id):
        """
        Delete user safely by removing dependent records first
        """

        
        self.cursor.execute(
            "DELETE FROM notifications WHERE user_id = ?",
            (user_id,)
        )

       

       
        self.cursor.execute(
            "DELETE FROM users WHERE user_id = ?",
            (user_id,)
        )

        self.conn.commit()

    def update_name(self, user_id, new_name):
     self.cursor.execute("""
        UPDATE users
        SET name = ?
        WHERE user_id = ?
     """, (new_name, user_id))
     self.conn.commit()
    
    def update_user(self, user_id, name, email):
     self.cursor.execute("""
        UPDATE users
        SET name = ?, email = ?
        WHERE user_id = ?
     """, (name, email, user_id))
     self.conn.commit()

    
