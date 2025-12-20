from flask import Flask
from config import Config
from database.create_tables import create_tables

from controllers.auth_controller import auth_bp
from controllers.course_controller import course_bp
from controllers.lecture_controller import lecture_bp
from controllers.assignment_controller import assignment_bp
from controllers.attendance_controller import attendance_bp
from controllers.admin_controller import admin_bp
from controllers.chat_controller import chat_bp
from controllers.file_controller import file_bp
from controllers.announcement_controller import announcement_bp
from controllers.notification_controller import notification_bp

def create_app():
    """Application Factory Pattern"""
    app = Flask(__name__, static_folder='src/static')
    app.config.from_object(Config)
    
    # Initialize app config
    Config.init_app(app)

    # Initialize database
    create_tables()

    # Register blueprints (modularization)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(course_bp, url_prefix="/courses")
    app.register_blueprint(lecture_bp, url_prefix="/lectures")
    app.register_blueprint(assignment_bp, url_prefix="/assignments")
    app.register_blueprint(attendance_bp, url_prefix="/attendance")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(file_bp, url_prefix="/file")
    app.register_blueprint(announcement_bp, url_prefix="/announcements")
    app.register_blueprint(notification_bp, url_prefix="/notifications")
    # Root route
    @app.route("/")
    def index():
        from flask import redirect, url_for
        return redirect(url_for("auth.login"))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)