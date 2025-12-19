from database.connection import DatabaseConnection

class BaseRepository:
    def __init__(self):
        db = DatabaseConnection()
        try:
            self.conn = db.get_connection()
            self.cursor = db.get_cursor()
        except Exception as e:
            print(f"[ERROR] Repository initialization failed: {e}")
            self.conn = None
            self.cursor = None
    
    def _ensure_connection(self):
        """Ensure database connection is available"""
        if self.conn is None or self.cursor is None:
            db = DatabaseConnection()
            self.conn = db.get_connection()
            self.cursor = db.get_cursor()
