from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.chat import chat_bp

app = Flask(__name__)
# enable cookies to be sent across origins (required for session handling)
# SAMESITE=None requires the cookie to be Secure per modern browser policies.
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
# CORS configuration
# We want to allow credentialed requests from the frontend.  During development
# we may deploy the frontend to various Netlify domains, so we don't hardcode a
# single origin here.  Flask-CORS will echo back the Origin header when
# supports_credentials=True, which satisfies the browser requirements.
# If you want to lock it down in production, set the CORS_ORIGINS
# environment variable to a comma-separated list of allowed origins.
import os
allowed = os.getenv("CORS_ORIGINS")
if allowed:
    origins = [o.strip() for o in allowed.split(",") if o.strip()]
else:
    origins = None  # None tells flask-cors to allow all origins

# explicitly include OPTIONS so flask-cors handles preflight requests
cors_args = dict(supports_credentials=True,
                 methods=["POST", "OPTIONS"],
                 allow_headers=["Content-Type"])
if origins is not None:
    cors_args["origins"] = origins

CORS(app, **cors_args)
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
