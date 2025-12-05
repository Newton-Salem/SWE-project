import mysql.connector
from mysql.connector import Error

class MySQLConnection:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "connection"): 
            try:
                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",     
                    database="edutrack"
                )
                self.cursor = self.connection.cursor(dictionary=True)
                print("MySQL Connected Successfull")

            except Error as e:
                print(f"Error connecting to MySQL: {e}")

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor
