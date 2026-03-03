from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.chat import chat_bp

app = Flask(__name__)
# enable cookies to be sent across origins (required for session handling)
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = False  # set True in production with HTTPS
CORS(app, supports_credentials=True)
app.secret_key = "super_secret_key_123"

app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True)
