from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.chat import chat_bp

app = Flask(__name__)
# enable cookies to be sent across origins (required for session handling)
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = False  # set True in production with HTTPS
# Only allow our frontend origin to make credentialed requests
CORS(app, supports_credentials=True,
     origins=["https://unrivaled-snickerdoodle-557c7f.netlify.app"])
app.secret_key = "super_secret_key_123"

# fallback in case flask-cors doesn't inject the header on some responses
@app.after_request
def _add_cors_credentials_header(response):
    if "Access-Control-Allow-Credentials" not in response.headers:
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True)
