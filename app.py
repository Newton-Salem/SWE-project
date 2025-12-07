from flask import Flask
from config import Config
from database.create_tables import create_tables

from controllers.auth_controller import auth_bp
from controllers.course_controller import course_bp
from controllers.lecture_controller import lecture_bp
from controllers.assignment_controller import assignment_bp
from controllers.attendance_controller import attendance_bp
from controllers.admin_controller import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    create_tables()

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(course_bp, url_prefix="/courses")
    app.register_blueprint(lecture_bp, url_prefix="/lectures")
    app.register_blueprint(assignment_bp, url_prefix="/assignments")
    app.register_blueprint(attendance_bp, url_prefix="/attendance")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)




