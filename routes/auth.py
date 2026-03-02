from flask import Blueprint, render_template, request, jsonify, session
import json
from utils.language_loader import get_mobile_prompt
from utils.otp_handler import generate_otp, verify_otp

auth_bp = Blueprint("auth", __name__)

with open("Data/JREDA_Farmer_context.json", encoding="utf-8") as f:
    FARMER_DATA = json.load(f)

@auth_bp.route("/")
def home():
    return render_template("index.html")

@auth_bp.route("/select-language", methods=["POST"])
def select_language():
    language = request.json.get("language")

    session.clear()
    session["language"] = language

    return jsonify({
        "message": get_mobile_prompt(language)
    })

@auth_bp.route("/verify-mobile", methods=["POST"])
def verify_mobile():
    mobile = request.json.get("mobile")

    session["mobile"] = mobile

    matched_farmer = None

    if isinstance(FARMER_DATA, dict):
        FARMER_DATA_LIST = [FARMER_DATA]
    else:
        FARMER_DATA_LIST = FARMER_DATA

    for farmer in FARMER_DATA_LIST:
        if farmer["mobile_number"] == mobile:
            matched_farmer = farmer
            break

    if matched_farmer:
        session["farmer_data"] = matched_farmer
        otp = generate_otp()
        session["otp"] = otp

        return jsonify({"status": "otp_sent"})
    else:
        return jsonify({"status": "not_registered"})

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_user_otp():
    user_otp = request.json.get("otp")
    real_otp = session.get("otp")

    if verify_otp(user_otp, real_otp):
        session["verified"] = True
        farmer = session.get("farmer_data")

        return jsonify({
            "status": "success",
            "farmer_name": farmer["farmer_name"],
            "pump_id": farmer["pump_id"],
            "vendor": farmer.get("vendor"),
            "district": farmer.get("district")
        })
    else:
        return jsonify({"status": "failed"})
