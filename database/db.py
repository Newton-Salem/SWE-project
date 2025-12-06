
import pyodbc

class MySQLConnection:   
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MySQLConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            try:
 
                self.connection = pyodbc.connect(
                    "DRIVER={ODBC Driver 17 for SQL Server};"
                    "SERVER=localhost;"       
                    "DATABASE=EduTrack;"     
                    "Trusted_Connection=yes;" 
                )
                self.cursor = self.connection.cursor()
                print("✔ Connected to SQL Server (Singleton)")
            except Exception as e:
                print("❌ Error connecting to SQL Server:", e)
                self.connection = None
                self.cursor = None

            self._initialized = True

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor
