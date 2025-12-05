from flask import Flask
from controllers.auth_controller import auth_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Register blueprints
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)
