# # services/track_grievance_service.py

# from services.gemini_service import generate_response


# def handle_track_grievance(session):
#     """
#     Handles Track Grievance button logic.
#     Tracks ONLY last grievance stored in session.
#     Fully LLM-driven. No hardcoded business responses.
#     """

#     # ✅ Verify session
#     if not session.get("verified"):
#         return "Please verify your mobile number first."

#     language = session.get("language", "English")
#     grievance = session.get("last_grievance")

#     # ✅ Case 1: No grievance in session
#     if not grievance:
#         prompt = f"""
# You are JREDA AI Assistant.

# The farmer is trying to track grievance,
# but no grievance has been raised in this session.

# Respond professionally in {language}.
# Keep response short and clear.
# Do NOT create fake grievance.
# """
#         return generate_response(prompt)

#     # ✅ Case 2: Grievance exists
#     prompt = f"""
# You are JREDA AI Assistant.

# Language must be strictly: {language}

# Below are the grievance details.
# Do NOT change values.
# Do NOT invent new data.
# Respond professionally and briefly.

# Grievance Details:
# Grievance ID: {grievance.get('Grievance ID')}
# ID: {grievance.get('ID')}
# Category: {grievance.get('Category')}
# Status: {grievance.get('Status')}
# Created Date: {grievance.get('Created Date')}
# Assigned Vendor: {grievance.get('Assigned Vendor')}
# Expected Resolution: {grievance.get('Expected Resolution')}

# Present clearly in this format:

# Grievance ID:
# Category:
# Status:
# Assigned Vendor:
# Expected Resolution:
# """

#     return generate_response(prompt)


# services/track_grievance_service.py

from services.gemini_service import generate_response


def handle_track_grievance(session):

    if not session.get("verified"):
        return generate_response(
            "Politely inform the user that they must verify their mobile number first."
        )

    language = session.get("language", "English")
    # Force Romanized Santali
    if language.lower() == "santali":
        language_instruction = "Romanized Santali (write Santali using English letters only, not Ol Chiki script)"
    else:
        language_instruction = language

    farmer_data = session.get("farmer_data", {})    
    
    
    farmer_data = session.get("farmer_data", {})

    grievance = session.get("last_grievance")

    # If not raised in session, check JSON-level grievance
    if not grievance and farmer_data.get("grievance_id"):
        grievance = {
            "Grievance ID": farmer_data.get("grievance_id"),
            "Category": farmer_data.get("grievance_category"),
            "Status": farmer_data.get("grievance_status"),
            "Created Date": farmer_data.get("grievance_created_date"),
            "Assigned Vendor": farmer_data.get("assigned_vendor"),
            "Expected Resolution": farmer_data.get("expected_resolution_date"),
            "Escalation Level": farmer_data.get("escalation_level") or "Not Escalated"
        }

        session["last_grievance"] = grievance

    # --------------------------------------------------
    # Build Prompt SAFELY (Always define prompt)
    # --------------------------------------------------

    if not grievance:
        prompt = f"""
You are JREDA AI Assistant.

Reply strictly in  {language_instruction}.
Be professional and short.

The farmer currently has NO registered grievance.

Politely inform them that:
- There is no active grievance found.
- They may use the Raise Grievance option if needed.
- If further help is required, contact JREDA helpline or visit https://jreda.com.
"""
    else:
        prompt = f"""
You are JREDA Government AI Assistant.

Reply strictly in {language_instruction}.
Be formal, professional and polite.
Use proper spacing between paragraphs.
Do NOT use bullet points.

Below are official grievance details of the farmer.
Do NOT modify values.
Do NOT invent any data.

Grievance Details:
Grievance ID: {grievance.get("Grievance ID")}
Category: {grievance.get("Category")}
Status: {grievance.get("Status")}
Created Date: {grievance.get("Created Date")}
Assigned Vendor: {grievance.get("Assigned Vendor")}
Expected Resolution: {grievance.get("Expected Resolution")}
Escalation Level: {grievance.get("Escalation Level")}

Response structure:

Start with:
"Here are the current details of your grievance:"

Then explain the grievance clearly in 2–3 short paragraphs.

After that, leave one blank line.

Then write exactly:

"If you need further assistance, you may contact the JREDA helpline or visit https://jreda.com."

On the next line, provide official contact details in this format:

Email: support@jreda.com  
Helpline: +91-XXXXXXXXXX

End politely as a government assistant.
"""

    return generate_response(prompt)