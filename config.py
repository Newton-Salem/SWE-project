import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SECURITY 
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-change-in-production"
    )

    #FILE UPLOADS

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR, "src", "static", "uploads"
    )

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

    #DATABASE 
    DB_SERVER = os.environ.get("DB_SERVER", "localhost")
    DB_NAME = os.environ.get("DB_NAME", "EduTrack")
    DB_DRIVER = os.environ.get("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    DB_TRUSTED = os.environ.get("DB_TRUSTED", "yes")

    # INIT 
    @staticmethod
    def init_app(app):
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)