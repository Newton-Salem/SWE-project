from controllers.assignment_controller import assignment_bp
from controllers.attendance_controller import attendance_bp
from controllers.chat_controller import chat_bp
from flask import Flask
from controllers.auth_controller import auth_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"


app.register_blueprint(auth_bp)
app.register_blueprint(assignment_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(chat_bp)


if __name__ == "__main__":
    app.run(debug=True)



