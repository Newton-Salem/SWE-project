from database.connection import MySQLConnection

class BaseRepository:
    def __init__(self):
        db = MySQLConnection()
        self.conn = db.get_connection()
        self.cursor = db.get_cursor()
