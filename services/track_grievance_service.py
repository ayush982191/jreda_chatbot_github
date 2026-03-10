# # # services/track_grievance_service.py

# # from services.gemini_service import generate_response


# # def handle_track_grievance(session):
# #     """
# #     Handles Track Grievance button logic.
# #     Tracks ONLY last grievance stored in session.
# #     Fully LLM-driven. No hardcoded business responses.
# #     """

# #     # ✅ Verify session
# #     if not session.get("verified"):
# #         return "Please verify your mobile number first."

# #     language = session.get("language", "English")
# #     grievance = session.get("last_grievance")

# #     # ✅ Case 1: No grievance in session
# #     if not grievance:
# #         prompt = f"""
# # You are JREDA AI Assistant.

# # The farmer is trying to track grievance,
# # but no grievance has been raised in this session.

# # Respond professionally in {language}.
# # Keep response short and clear.
# # Do NOT create fake grievance.
# # """
# #         return generate_response(prompt)

# #     # ✅ Case 2: Grievance exists
# #     prompt = f"""
# # You are JREDA AI Assistant.

# # Language must be strictly: {language}

# # Below are the grievance details.
# # Do NOT change values.
# # Do NOT invent new data.
# # Respond professionally and briefly.

# # Grievance Details:
# # Grievance ID: {grievance.get('Grievance ID')}
# # ID: {grievance.get('ID')}
# # Category: {grievance.get('Category')}
# # Status: {grievance.get('Status')}
# # Created Date: {grievance.get('Created Date')}
# # Assigned Vendor: {grievance.get('Assigned Vendor')}
# # Expected Resolution: {grievance.get('Expected Resolution')}

# # Present clearly in this format:

# # Grievance ID:
# # Category:
# # Status:
# # Assigned Vendor:
# # Expected Resolution:
# # """

# #     return generate_response(prompt)


# # services/track_grievance_service.py

# from services.gemini_service import generate_response


# import requests

# def handle_track_grievance(session):

#     if not session.get("verified"):
#         return generate_response(
#             "Please verify your mobile number first before tracking grievance."
#         )

#     grievance_id = session.get("track_grievance_id")

#     if not grievance_id:
#         return generate_response("Please provide your Grievance ID to track status.")

#     try:
#         # 🔹 Call your real GET API (which returns array)
#         api_url = "http://your-api-url.com/get-grievances"
#         response = requests.get(api_url)

#         if response.status_code != 200:
#             return generate_response("Unable to fetch grievance details right now.")

#         grievances = response.json()   # This is ARRAY

#         if not isinstance(grievances, list):
#             return generate_response("Invalid data format received from server.")

#         # 🔹 Filter by grievance_id
#         grievance = next(
#             (g for g in grievances if g.get("grievance_id") == grievance_id),
#             None
#         )

#         if not grievance:
#             return generate_response(
#                 f"No grievance found with ID {grievance_id}."
#             )

#         # 🔹 Format response
#         reply = f"""
# Here are your grievance details:

# Grievance ID: {grievance.get('grievance_id')}
# Category: {grievance.get('category')}
# Status: {grievance.get('current_status')}
# Created Date: {grievance.get('created_date')}
# Assigned Vendor: {grievance.get('assigned_vendor')}
# Expected Resolution: {grievance.get('expected_resolution_date')}
# Escalation Level: {grievance.get('escalation_level')}
#         """

#         return reply.strip()

#     except Exception as e:
#         print("Error:", str(e))
#         return generate_response(
#             "Something went wrong while fetching grievance details."
#         )

#     # --------------------------------------------------
#     # Build Prompt SAFELY (Always define prompt)
#     # --------------------------------------------------

#     if not grievance:
#         prompt = f"""
# You are JREDA AI Assistant.

# Reply strictly in  {language_instruction}.
# Be professional and short.

# The farmer currently has NO registered grievance.

# Politely inform them that:
# - There is no active grievance found.
# - They may use the Raise Grievance option if needed.
# - If further help is required, contact JREDA helpline or visit https://jreda.com.
# """
#     else:
#         prompt = f"""
# You are JREDA Government AI Assistant.

# Reply strictly in {language_instruction}.
# Be formal, professional and polite.
# Use proper spacing between paragraphs.
# Do NOT use bullet points.

# Below are official grievance details of the farmer.
# Do NOT modify values.
# Do NOT invent any data.

# Grievance Details:
# Grievance ID: {grievance.get("Grievance ID")}
# Category: {grievance.get("Category")}
# Status: {grievance.get("Status")}
# Created Date: {grievance.get("Created Date")}
# Assigned Vendor: {grievance.get("Assigned Vendor")}
# Expected Resolution: {grievance.get("Expected Resolution")}
# Escalation Level: {grievance.get("Escalation Level")}

# Response structure:

# Start with:
# "Here are the current details of your grievance:"

# Then explain the grievance clearly in 2–3 short paragraphs.

# After that, leave one blank line.

# Then write exactly:

# "If you need further assistance, you may contact the JREDA helpline or visit https://jreda.com."

# On the next line, provide official contact details in this format:

# Email: support@jreda.com  
# Helpline: +91-XXXXXXXXXX

# End politely as a government assistant.
# """

#     return generate_response(prompt)


# services/track_grievance_service.py
# services/track_grievance_service.py

import requests
from services.gemini_service import generate_response

def handle_track_grievance(session):
    """
    Handles Track Grievance flow.
    - Takes grievance_id from session
    - Calls real GET API (returns array)
    - Filters by grievance_id
    - Returns formatted response
    - Does NOT use LLM
    """

    # --------------------------------------------------
    # 1️⃣ Verify User Session
    # --------------------------------------------------
    if not session.get("verified"):
        return "Please verify your mobile number first."

    grievance_id = session.get("track_grievance_id")

    if not grievance_id:
        return "Please provide a valid Grievance ID."

    try:
        # --------------------------------------------------
        # 2️⃣ Call Real GET API (returns ARRAY)
        # --------------------------------------------------
        api_url = "https://sheetdb.io/api/v1/uj1y32yara8fx"

        response = requests.get(api_url, timeout=10)

        if response.status_code != 200:
            return "Unable to fetch grievance details at the moment. Please try again later."

        grievances = response.json()

        if not isinstance(grievances, list):
            return "Invalid data received from grievance server."

        # --------------------------------------------------
        # 3️⃣ Filter grievance by ID
        # --------------------------------------------------
        grievance = next(
            (g for g in grievances if g.get("grievance_id") == grievance_id),
            None
        )

        if not grievance:
            return f"No grievance found with ID {grievance_id}. Please check and try again."

        # --------------------------------------------------
        # 4️⃣ Build Clean Response (No LLM)
        # --------------------------------------------------
        reply = f"""
Grievance Details

Grievance ID: {grievance.get('grievance_id')}
Farmer ID: {grievance.get('farmer_id')}
Pump ID: {grievance.get('pump_id')}
Category: {grievance.get('category')}
Status: {grievance.get('current_status')}
Created Date: {grievance.get('created_date')}
SLA (Hours): {grievance.get('sla_hours')}
Assigned Vendor: {grievance.get('assigned_vendor')}
Expected Resolution: {grievance.get('expected_resolution_date')}
Escalation Level: {grievance.get('escalation_level')}
Last Updated: {grievance.get('updated_date')}

If you need further assistance, please contact JREDA helpline.
"""

        return reply.strip()

    # --------------------------------------------------
    # 5️⃣ API Connection Error
    # --------------------------------------------------
    except requests.exceptions.RequestException as e:
        print("API Error:", str(e))
        return "There was a technical issue while connecting to the grievance system. Please try again later."

    # --------------------------------------------------
    # 6️⃣ Unexpected Error
    # --------------------------------------------------
    except Exception as e:
        print("Unexpected Error:", str(e))
        return "Something went wrong while tracking your grievance. Please try again later."