import os

try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False
    print("[WARNING] pyodbc not installed. Install it with: pip install pyodbc")

class DatabaseConnection:
    """Singleton pattern for database connection - SQL Server"""
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not DatabaseConnection._initialized:
            if not PYODBC_AVAILABLE:
                print("[ERROR] pyodbc is not installed. Please install it with: pip install pyodbc")
                self.connection = None
                self.cursor = None
                DatabaseConnection._initialized = True
                return
            
            try:
                # SQL Server connection details
                server = os.environ.get("DB_SERVER", "host.docker.internal")  # Docker on Windows
                database = os.environ.get("DB_NAME", "EduTrack")
                driver = os.environ.get("DB_DRIVER", "ODBC Driver 18 for SQL Server")
                user = os.environ.get("DB_USER", "sa")
                password = os.environ.get("DB_PASSWORD", "StrongPassword123!")

                # Check available drivers
                available_drivers = pyodbc.drivers()
                if driver not in available_drivers:
                    print(f"[WARNING] Driver '{driver}' not found. Available drivers: {', '.join(available_drivers)}")
                    sql_drivers = [d for d in available_drivers if "SQL Server" in d]
                    if sql_drivers:
                        driver = sql_drivers[0]
                        print(f"[INFO] Using driver: {driver}")
                    else:
                        raise Exception("No SQL Server ODBC driver found. Please install an ODBC Driver for SQL Server.")

                # Build connection string for SQL Authentication
                connection_string = (
                    f"DRIVER={{{driver}}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={user};"
                    f"PWD={password};"
                    "Encrypt=no;"  
                )


                print(f"Attempting to connect to SQL Server: {server}/{database}")
                self.connection = pyodbc.connect(connection_string, timeout=10)
                self.cursor = self.connection.cursor()
                print("[OK] Connected to SQL Server successfully")
                DatabaseConnection._initialized = True

            except Exception as e:
                print(f"[ERROR] Could not connect to SQL Server: {type(e).__name__}: {e}")
                print("Check that:")
                print("  1. SQL Server is running and reachable from Docker")
                print("  2. SQL Authentication user/password are correct")
                print("  3. Database exists")
                print("  4. ODBC Driver is installed")
                self.connection = None
                self.cursor = None
                DatabaseConnection._initialized = True

    def get_connection(self):
        if self.connection is None:
            raise Exception("Database connection is not available. Check your SQL Server configuration.")
        return self.connection

    def get_cursor(self):
        if self.cursor is None:
            raise Exception("Database cursor is not available. Check your SQL Server configuration.")
        return self.cursor

    def commit(self):
        if self.connection:
            try:
                self.connection.commit()
            except Exception as e:
                print(f"[ERROR] Error committing transaction: {e}")
                raise
        else:
            raise Exception("Cannot commit: Database connection is not available.")

    def close(self):
        if self.connection:
            try:
                self.connection.close()
            except Exception as e:
                print(f"[WARNING] Error closing connection: {e}")

    def is_connected(self):
        """Check if database connection is available"""
        return self.connection is not None and self.cursor is not None
