# # from flask import Blueprint, request, jsonify, session
# # from services.gemini_service import build_prompt, generate_response
# # from services.grievance_service import store_grievance
# # from services.speech_service import text_to_speech
# # from services.track_grievance_service import handle_track_grievance

# # chat_bp = Blueprint("chat", __name__)


# # @chat_bp.route("/chat", methods=["POST"])
# # def chat():

# #     if not session.get("verified"):
# #         return jsonify({"reply": "Please verify your mobile number first."})

# #     user_input = request.json.get("message", "")
# #     schema = request.json.get("schema")

# #     language = session.get("language", "English")
# #     farmer_context = session.get("farmer_data")

# #     clean_input = user_input.strip().lower()

# #     # ===================================================
# #     # ✅ HANDLE TRACK BUTTON CLICK
# #     # ===================================================
# #     if user_input == "ACTION_TRACK_GRIEVANCE":

# #         session["mode"] = "track"   # store mode safely

# #         reply = handle_track_grievance(session)

# #         lang_code = {
# #             "English": "en",
# #             "Hindi": "hi",
# #             "Bengali": "bn",
# #             "Santali": "en"
# #         }.get(language, "en")

# #         audio_base64 = text_to_speech(reply, lang_code)

# #         return jsonify({
# #             "reply": reply,
# #             "audio": audio_base64
# #         })

# #     # ===================================================
# #     # 🚫 BLOCK CREATION INSIDE TRACK MODE
# #     # ===================================================
# #     current_mode = session.get("mode")

# #     if current_mode == "track":

# #         create_keywords = ["create", "new ticket", "raise", "new grievance"]

# #         if any(word in clean_input for word in create_keywords):

# #             prompt = f"""
# # You are JREDA AI Assistant.

# # User is currently viewing grievance tracking details.

# # Politely inform that:
# # - This section is only for tracking existing grievances.
# # - To create a new grievance, use the Raise Grievance option in this AI chatbot
# #   or visit https://jreda.com.

# # Respond professionally in {language}.
# # Keep it short and clear.
# # """

# #             reply = generate_response(prompt)

# #             lang_code = {
# #                 "English": "en",
# #                 "Hindi": "hi",
# #                 "Bengali": "bn",
# #                 "Santali": "en"
# #             }.get(language, "en")

# #             audio_base64 = text_to_speech(reply, lang_code)

# #             return jsonify({
# #                 "reply": reply,
# #                 "audio": audio_base64
# #             })

# #     # ===================================================
# #     # NORMAL LLM FLOW
# #     # ===================================================

# #     confirmation_keywords = [
# #         "yes", "haan", "ha", "ok", "okay",
# #         "sure", "please proceed", "go ahead"
# #     ]

# #     is_confirmation = any(word in clean_input for word in confirmation_keywords)

# #     if schema and not is_confirmation:
# #         session["last_issue"] = user_input

# #     prompt = build_prompt(
# #         user_input=user_input,
# #         language=language,
# #         verified=True,
# #         farmer_context=farmer_context,
# #         schema=schema,
# #         last_grievance=session.get("last_grievance")
# #     )

# #     reply = generate_response(prompt)

# #     # ===================================================
# #     # HANDLE GRIEVANCE CREATION
# #     # ===================================================

# #     if "RAISE_GRIEVANCE_APPROVED" in reply:

# #         session["mode"] = "raise"  # clear track mode safely

# #         issue_summary = session.get("last_issue", "Issue description not provided")

# #         data = {}
# #         for line in reply.split("\n"):
# #             if ":" in line:
# #                 k, v = line.split(":", 1)
# #                 data[k.strip()] = v.strip()

# #         record = store_grievance(
# #             {
# #                 "Category": data.get("Category"),
# #                 "Issue Summary": issue_summary
# #             },
# #             farmer_context
# #         )

# #         session["last_grievance"] = record
# #         session.pop("last_issue", None)

# #         reply = (
# #             "Grievance Created Successfully\n\n"
# #             f"Grievance ID: {record['Grievance ID']}\n"
# #             f"ID: {record['ID']}\n"
# #             f"Mobile Number: {farmer_context.get('mobile_number')}\n"
# #             f"Category: {record['Category']}\n"
# #             f"Status: {record['Status']}\n"
# #             f"Created Date: {record['Created Date']}\n"
# #             f"Assigned Vendor: {record['Assigned Vendor']}\n"
# #             f"Expected Resolution: {record['Expected Resolution']}\n"
# #             f"Issue Summary: {issue_summary}\n\n"
# #             "If you have any other enquiry, please feel free to ask."
# #         )

# #     # ===================================================
# #     # TEXT TO SPEECH
# #     # ===================================================

# #     lang_code = {
# #         "English": "en",
# #         "Hindi": "hi",
# #         "Bengali": "bn",
# #         "Santali": "en"
# #     }.get(language, "en")

# #     audio_base64 = text_to_speech(reply, lang_code)

# #     return jsonify({
# #         "reply": reply,
# #         "audio": audio_base64
# #     })


# #--------------------------------------------------------------------------------------*************************------------
# # from flask import Blueprint, request, jsonify, session
# # from services.gemini_service import build_prompt, generate_response
# # from services.grievance_service import store_grievance
# # from services.speech_service import text_to_speech
# # from services.track_grievance_service import handle_track_grievance
# # import re
# # from services.scheme_service import handle_scheme_query
# # from services.device_service import handle_device_status


# # chat_bp = Blueprint("chat", __name__)


# # @chat_bp.route("/chat", methods=["POST"])
# # def chat():

# #     if not session.get("verified"):
# #         return jsonify({"reply": "Please verify your mobile number first."})

# #     user_input = request.json.get("message", "")
# #     schema = request.json.get("schema")

# #     language = session.get("language", "English")
# #     farmer_context = session.get("farmer_data")

# #     clean_input = user_input.strip()
# #     lower_input = clean_input.lower()
# #     upper_input = clean_input.upper()

# #     # Language code for TTS
# #     lang_code = {
# #         "English": "en",
# #         "Hindi": "hi",
# #         "Bengali": "bn",
# #         "Santali": "en"
# #     }.get(language, "en")

# #     # ===================================================
# #     # ✅ TRACK BUTTON CLICK
# #     # ===================================================

# #     if user_input == "ACTION_TRACK_GRIEVANCE":
# #         session["mode"] = "track"
# #         reply = handle_track_grievance(session)
# #         audio_base64 = text_to_speech(reply, lang_code)
# #         return jsonify({"reply": reply, "audio": audio_base64})

# #     # ===================================================
# #     # ✅ DETECT TICKET ID (ANTI-HALLUCINATION FIX)
# #     # ===================================================

# #     ticket_pattern = r"\bGRV\d+\b"
# #     match = re.search(ticket_pattern, upper_input)

# #     if match:
# #         ticket_id = match.group()

# #         grievance = session.get("last_grievance")

# #         if grievance and grievance.get("Grievance ID") == ticket_id:

# #             prompt = f"""
# # You are JREDA Government AI Assistant.

# # Reply strictly in {language}.
# # Use ONLY the grievance data provided below.
# # Do NOT say record not found.
# # Do NOT invent any information.
# # Keep response concise and professional.

# # Grievance Data:
# # Grievance ID: {grievance.get("Grievance ID")}
# # Category: {grievance.get("Category")}
# # Status: {grievance.get("Status")}
# # Created Date: {grievance.get("Created Date")}
# # Assigned Vendor: {grievance.get("Assigned Vendor")}
# # Expected Resolution: {grievance.get("Expected Resolution")}
# # Escalation Level: {grievance.get("Escalation Level")}

# # User Question:
# # {user_input}
# # """

# #             reply = generate_response(prompt)
# #             audio_base64 = text_to_speech(reply, lang_code)
# #             return jsonify({"reply": reply, "audio": audio_base64})

# #         else:
# #             # If ticket ID does not match session record
# #             prompt = f"""
# # You are JREDA Government AI Assistant.

# # Reply strictly in {language}.
# # Politely inform the user that no grievance with ID {ticket_id} was found in the current records.
# # Advise them to verify the ID or contact JREDA support.
# # """

# #             reply = generate_response(prompt)
# #             audio_base64 = text_to_speech(reply, lang_code)
# #             return jsonify({"reply": reply, "audio": audio_base64})

# #     # ===================================================
# #     # 🚫 BLOCK CREATION INSIDE TRACK MODE
# #     # ===================================================

# #     current_mode = session.get("mode")

# #     if current_mode == "track":
# #         create_keywords = ["create", "new ticket", "raise", "new grievance"]

# #         if any(word in clean_input.lower() for word in create_keywords):

# #             prompt = f"""
# # You are JREDA AI Assistant.

# # User is currently viewing grievance tracking details.

# # Politely inform that:
# # - This section is only for tracking existing grievances.
# # - To create a new grievance, use the Raise Grievance option in this AI chatbot
# #   or visit https://jreda.com.

# # Respond professionally in {language}.
# # Keep it short and clear.
# # """

# #             reply = generate_response(prompt)
# #             audio_base64 = text_to_speech(reply, lang_code)
# #             return jsonify({"reply": reply, "audio": audio_base64})
        
# #     # ===================================================
# # # SCHEME DETAILS FLOW
# # # ===================================================

# #     scheme_options = [
# #     "Eligibility & Conditions",
# #     "Subsidy Status",
# #     "How to Apply",
# #     "Contact Details",
# #     "Registration"
# #     ]

# #     if schema and user_input.strip() in scheme_options:

# #         # 🔥 Store scheme conversation context
# #         session["active_scheme"] = schema
# #         session["active_scheme_topic"] = user_input.strip()

# #         reply = handle_scheme_query(schema, user_input.strip(), language)

# #         audio_base64 = text_to_speech(reply, lang_code)

# #         return jsonify({
# #             "reply": reply,
# #             "audio": audio_base64
# #         })
    
# # # ===================================================
# # # SCHEME FOLLOW-UP (CONTEXT CONTINUATION)
# # # ===================================================

# #     if session.get("active_scheme"):

# #         # Avoid re-triggering main scheme option block
# #         scheme_options = [
# #             "Eligibility & Conditions",
# #             "Subsidy Status",
# #             "How to Apply",
# #             "Contact Details",
# #             "Registration"
# #         ]

# #         # If user input is NOT one of main scheme buttons,
# #         # treat it as follow-up question
# #         if user_input.strip() not in scheme_options:

# #             follow_up_prompt = f"""
# #     You are JREDA Government AI Assistant.

# #     The user is currently discussing:

# #     Scheme: {session.get("active_scheme")}
# #     Topic: {session.get("active_scheme_topic")}

# #     User Follow-up Question:
# #     {user_input}

# #     Continue the explanation based on the same scheme and topic.
# #     Do NOT switch to grievance handling.
# #     Do NOT ask the user to explain their issue.
# #     Be professional, structured and concise.
# #     Use numbered points if needed.
# #     Do not use markdown symbols like **.
# #     """

# #             reply = generate_response(follow_up_prompt)

# #             audio_base64 = text_to_speech(reply, lang_code)

# #             return jsonify({
# #                 "reply": reply,
# #                 "audio": audio_base64
# #             })
        
# #     # ===================================================
# # # DEVICE STATUS FLOW
# # # ===================================================

# #     # ===================================================
# # # DEVICE STATUS FLOW
# # # ===================================================

# #     if user_input == "SOLAR_PUMP_STATUS":

# #         session["device_mode"] = True   # 🔥 LOCK SESSION

# #         farmer_context = session.get("farmer_data")

# #         reply = handle_device_status(farmer_context, language)

# #         audio_base64 = text_to_speech(reply, lang_code)

# #         return jsonify({
# #             "reply": reply,
# #             "audio": audio_base64
# #         })
    
# #     # ===================================================
# # # DEVICE FOLLOW-UP SESSION (STRICT MODE)
# # # ===================================================

# #     if session.get("device_mode"):

# #         farmer_context = session.get("farmer_data")

# #         device_prompt = f"""
# #     You are JREDA Government AI Assistant.

# #     The user is currently viewing Solar Pump Status information.

# #     You must ONLY answer questions related to the pump status,
# #     voltage, power status, warranty, fault codes, or device diagnostics.

# #     If the user asks anything unrelated to pump status,
# #     respond strictly with:

# #     "This section is only for Solar Pump Status queries. For other assistance, please use the main AI assistant or visit https://jreda.com."

# #     Device Data:
# #     Pump ID: {farmer_context.get("pump_id")}
# #     Pump Status: {farmer_context.get("pump_status")}
# #     Voltage: {farmer_context.get("voltage")}
# #     Power Status: {farmer_context.get("power_status")}
# #     Warranty Status: {farmer_context.get("warranty_status")}
# #     Fault Code: {farmer_context.get("fault_code")}
# #     Alarm Status: {farmer_context.get("alarm_status")}

# #     User Question:
# #     {user_input}

# #     Keep response concise and professional.
# #     If user asks to summarize or explain in 2 lines, follow that format.
# #     Do NOT act as a general chatbot.
# #     """

# #         reply = generate_response(device_prompt)

# #         audio_base64 = text_to_speech(reply, lang_code)

# #         return jsonify({
# #             "reply": reply,
# #             "audio": audio_base64
# #         })

# #     # ===================================================
# #     # NORMAL LLM FLOW
# #     # ===================================================

# #     # ==========================================
# # # MULTI-LANGUAGE CONFIRMATION DETECTION
# # # ==========================================

# #     confirmation_words = [
# #         # English
# #         "yes", "ok", "okay", "sure",

# #         # Hindi
# #         "haan", "ha", "haa", "हाँ",

# #         # Bengali
# #         "হ্যাঁ",

# #         # Santali (Roman)
# #         "haan"
# #     ]

# #     lower_input = clean_input.lower()

# #     is_confirmation = lower_input in confirmation_words


# #     # ==========================================
# #     # STORE ISSUE ONLY WHEN USER IS DESCRIBING
# #     # ==========================================

# #     if schema and not is_confirmation and not session.get("awaiting_confirmation"):
# #         session["last_issue"] = user_input


# #     # ==========================================
# #     # IF WAITING FOR CONFIRMATION → HANDLE DIRECTLY
# #     # ==========================================

# #     if session.get("awaiting_confirmation") and is_confirmation:

# #         session["awaiting_confirmation"] = False

# #         reply = f"""
# #     RAISE_GRIEVANCE_APPROVED
# #     Category: {schema}
# #     Issue Summary: {session.get("last_issue", "")}
# #     """

# #     else:

# #         prompt = build_prompt(
# #             user_input=user_input,
# #             language=language,
# #             verified=True,
# #             farmer_context=farmer_context,
# #             schema=schema,
# #             last_grievance=session.get("last_grievance")
# #         )

# #         reply = generate_response(prompt)

# #         # If LLM is asking for confirmation → lock state
# #         if (
# #             "raise grievance" in reply.lower() or
# #             "शिकायत दर्ज" in reply or
# #             "অভিযোগ" in reply or
# #             "abhijog" in reply.lower()
# #         ):
# #             session["awaiting_confirmation"] = True

# #     # ===================================================
# #     # HANDLE GRIEVANCE CREATION
# #     # ===================================================

# #     if "RAISE_GRIEVANCE_APPROVED" in reply:

# #         issue_summary = session.get("last_issue", "")

# #         data = {}
# #         for line in reply.split("\n"):
# #             if ":" in line:
# #                 k, v = line.split(":", 1)
# #                 data[k.strip()] = v.strip()

# #         record = store_grievance(
# #             {
# #                 "Category": data.get("Category"),
# #                 "Issue Summary": issue_summary
# #             },
# #             farmer_context
# #         )

# #         session["last_grievance"] = record
# #         session.pop("last_issue", None)

# #         language = session.get("language", "English")

# #         # ==================================
# #         # CLEAN GOVERNMENT FORMAT RESPONSE
# #         # ==================================

# #         final_prompt = f"""
# #     You are JREDA Government AI Assistant.

# #     IMPORTANT:
# #     Reply ONLY in {language}.
# #     Do NOT use markdown.
# #     Do NOT use bold.
# #     Use plain professional government format.

# #     STRUCTURE EXACTLY:

# #     Line 1:
# #     Grievance Confirmation (translate in {language})

# #     Blank line.

# #     Grievance ID: {record['Grievance ID']}
# #     Category: {record['Category']}
# #     Status: {record['Status']}
# #     Created Date: {record['Created Date']}
# #     Assigned Vendor: {record['Assigned Vendor']}
# #     Expected Resolution: {record['Expected Resolution']}

# #     Blank line.

# #     Issue Summary:

# #     ⚠ Keep the heading "Issue Summary:" in English.
# #     Do NOT translate it.

# #     After that heading, write explanation in {language}:
# #     - What issue farmer is facing
# #     - Possible reason
# #     - Formal tone
# #     - Concise explanation
# #     """

# #         reply = generate_response(final_prompt)

# #         # Safety cleanup
# #         reply = reply.replace("**", "")
# #         reply = reply.replace("*", "")
# #         reply = reply.replace("समस्या का सारांश:", "Issue Summary:")
# #         reply = reply.replace("সমস্যার সারাংশ:", "Issue Summary:")

# #         # Reset conversation state
# #         session["awaiting_confirmation"] = False
# #         session["mode"] = None
# #         session["device_mode"] = False

        

            

# #         audio_base64 = text_to_speech(reply, lang_code)

# #         return jsonify({
# #             "reply": reply,
# #             "audio": audio_base64
# #         })


# #--------------------------------------------------------------------------------------

# from flask import Blueprint, request, jsonify, session
# from services.gemini_service import generate_response
# from services.grievance_service import store_grievance
# from services.speech_service import text_to_speech
# from services.track_grievance_service import handle_track_grievance
# from services.scheme_service import handle_scheme_query
# from services.device_service import handle_device_status
# import re

# chat_bp = Blueprint("chat", __name__)


# @chat_bp.route("/chat", methods=["POST"])
# def chat():

#     # =====================================================
#     # VERIFY MOBILE FIRST
#     # =====================================================
#     # ================= GUEST ACCESS CONTROL =================
#     if not session.get("verified"):

#         schema = request.json.get("schema")
#         user_input = request.json.get("message", "").strip()
#         language = session.get("language", "English")

#         allowed_options = [
#             "Eligibility & Conditions",
#             "Benefits",
#             "How to Apply",
#             "Contact Details",
#             "Registration"
#         ]

#         # 1️⃣ Allow first scheme option click
#         if schema and user_input in allowed_options:
#             reply = handle_scheme_query(schema, user_input, language)
#             return jsonify({"reply": reply})

#         # 2️⃣ Allow follow-up questions AFTER scheme is selected
#         if schema:
#             reply = handle_scheme_query(schema, user_input, language)
#             return jsonify({"reply": reply})

#         # Otherwise block
#         return jsonify({"reply": "Please verify your mobile number first."})

#     user_input = request.json.get("message", "").strip()
#     schema = request.json.get("schema")

#     language = session.get("language", "English")
#     if language.lower() == "santali":
#         language_instruction = "Romanized Santali (write Santali using English letters only, not Ol Chiki script)"
#     else:
#         language_instruction = language
   
#     farmer_context = session.get("farmer_data")

#     # lang_code = {
#     #     "English": "en",
#     #     "Hindi": "hi",
#     #     "Bengali": "bn",
#     #     "Santali": "en"
#     # }.get(language, "en")

#     import re
#     lower_input = re.sub(r'[^\w\s]', '', user_input.lower()).strip()

#     # =====================================================
#     # TRACK GRIEVANCE BUTTON
#     # =====================================================
#     if user_input == "ACTION_TRACK_GRIEVANCE":
#         session["mode"] = "track"
#         reply = handle_track_grievance(session)
#         # audio = text_to_speech(reply, language)
#         return jsonify({"reply": reply})

#     # =====================================================
#     # DEVICE STATUS BUTTON
#     # =====================================================
#     if user_input == "SOLAR_PUMP_STATUS":
#         reply = handle_device_status(farmer_context, language)
#         #audio = text_to_speech(reply, language)
#         return jsonify({"reply": reply})

#     # =====================================================
#     # SCHEME DETAILS FLOW
#     # =====================================================
#     scheme_options = [
#         "Eligibility & Conditions",
#         "Subsidy Status",
#         "How to Apply",
#         "Contact Details",
#         "Registration"
#     ]

#     if schema and user_input.strip() in scheme_options:

#         # Reset grievance flow
#         session["awaiting_confirmation"] = False
#         session.pop("last_issue", None)

#         reply = handle_scheme_query(schema, user_input.strip(), language)
#         audio = text_to_speech(reply, language)

#         return jsonify({"reply": reply, "audio": audio})

#     # =====================================================
#     # CONFIRMATION WORDS
#     # =====================================================
#     confirmation_words = [
#         "yes", "ok", "okay", "sure",
#         "haan", "ha", "haa", "हाँ",
#         "হ্যাঁ"
#     ]

#     is_confirmation = any(word in lower_input for word in confirmation_words)

#     # =====================================================
#     # STEP 1: USER DESCRIBES ISSUE
#     # =====================================================
#     if schema and not session.get("awaiting_confirmation") and user_input.strip() not in scheme_options:
 
#         session["last_issue"] = user_input
#         session["awaiting_confirmation"] = True
 
#         solution_prompt = f"""
# You are JREDA Government AI Assistant.
 
# User issue:
# {user_input}
 
# Provide:
# 1. Brief troubleshooting guidance.
# 2. Then politely ask if user wants to raise grievance.
 
# Reply strictly in {language}.
# No markdown.
# No bold.
# Professional tone.
# """
 
#         reply = generate_response(solution_prompt)
#         #audio = text_to_speech(reply, language)
#         return jsonify({"reply": reply})
 
#     # =====================================================
#     # STEP 2: USER CONFIRMS → CREATE GRIEVANCE
#     # =====================================================
#     if session.get("awaiting_confirmation") and is_confirmation:
 
#         issue_text = session.get("last_issue", "")
 
#         # =========================================
#         # STEP A: Generate LLM Issue Summary
#         # =========================================
#         summary_prompt = f"""
# You are JREDA Government AI Assistant.
 
# Summarize the user's issue professionally.
 
# User Reported Issue:
# {issue_text}
 
# Rules:
# - Do NOT add any heading.
# - Do NOT write "Issue Summary:".
# - Only return the explanation paragraph.
# - Mention possible technical reason.
# - Keep concise.
# - Reply strictly in {language}.
# - No markdown.
# - No bold.
# """
 
#         llm_summary = generate_response(summary_prompt)
 
#         # =========================================
#         # STEP B: Store grievance using LLM summary
#         # =========================================
#         record = store_grievance(
#             {
#                 "Category": schema,
#                 "Issue Summary": llm_summary   # ✅ LLM GENERATED SUMMARY
#             },
#             farmer_context
#         )
 
#         session["awaiting_confirmation"] = False
#         session.pop("last_issue", None)
 
 
#         reply = f"""
#         Grievance Confirmation
 
#         Grievance ID: {record.get('grievance_id')}
#         Mobile Number: {record.get('mobile_number')}
#         Pump ID: {record.get('pump_id')}
#         Category: {record.get('category')}
#         Status: {record.get('current_status')}
#         Created Date: {record.get('created_date')}
#         Assigned Vendor: {record.get('assigned_vendor')}
#         Expected Resolution: {record.get('expected_resolution_date')}
 
#         Issue Summary:
#         {llm_summary}
#         """
 
#         #audio = text_to_speech(reply, language)
 
#         return jsonify({"reply": reply})
 
#     # =====================================================
#     # DEFAULT NORMAL RESPONSE
#     # =====================================================
#     general_prompt = f"""
#     You are JREDA Government AI Assistant.
 
#     Reply strictly in {language}.
#     No markdown.
#     Professional tone.
 
#     IMPORTANT DOMAIN RULE:
 
#     You are ONLY allowed to answer questions related to:
#     - JREDA schemes
#     - PM-KUSUM
#     - Solar pumps
#     - Grievance registration
#     - Grievance tracking
#     - Device status
#     - Renewable energy programs under JREDA
 
#     If the user asks anything unrelated to JREDA or solar services,
#     politely refuse and guide them back to the available options.
 
#     For unrelated questions, reply like:
#     "This assistant is dedicated to JREDA solar services only. Please choose the available options only."
 
#     User message:
#     {user_input}
#     """
 
#     reply = generate_response(general_prompt)
#     #audio = text_to_speech(reply, language)
 
#     return jsonify({"reply": reply})

from flask import Blueprint, request, jsonify, session
from services.gemini_service import generate_response
from services.grievance_service import store_grievance
# from services.speech_service import text_to_speech
from services.track_grievance_service import handle_track_grievance
from services.scheme_service import handle_scheme_query
from services.device_service import handle_device_status
import re
 
chat_bp = Blueprint("chat", __name__)
 
 
@chat_bp.route("/chat", methods=["POST"])
def chat():
 
    # =====================================================
    # VERIFY MOBILE FIRST
    # =====================================================
    # ================= GUEST ACCESS CONTROL =================
    if not session.get("verified"):
 
        schema = request.json.get("schema")
        user_input = request.json.get("message", "").strip()
        language = session.get("language", "English")
 
        allowed_options = [
            "Eligibility & Conditions",
            "Benefits",
            "How to Apply",
            "Contact Details",
            "Registration"
        ]
 
        # 1️⃣ Allow first scheme option click
        if schema and user_input in allowed_options:
            reply = handle_scheme_query(schema, user_input, language)
            return jsonify({"reply": reply})
 
        # 2️⃣ Allow follow-up questions AFTER scheme is selected
        if schema:
            reply = handle_scheme_query(schema, user_input, language)
            return jsonify({"reply": reply})
 
        # Otherwise block
        return jsonify({"reply": "Please verify your mobile number first."})
 
    user_input = request.json.get("message", "").strip()
    schema = request.json.get("schema")
 
    language = session.get("language", "English")
    # Force correct language rules
    if language.lower() == "santali":
        language_instruction = "Romanized Santali (write Santali using English letters only, not Ol Chiki script)"
    else:
        language_instruction = language
    farmer_context = session.get("farmer_data")
 
    # lang_code = {
    #     "English": "en",
    #     "Hindi": "hi",
    #     "Bengali": "bn",
    #     "Santali": "en"
    # }.get(language, "en")
 
    import re
    lower_input = re.sub(r'[^\w\s]', '', user_input.lower()).strip()
 
    # =====================================================
    # TRACK GRIEVANCE BUTTON
    # =====================================================
    if user_input == "ACTION_TRACK_GRIEVANCE":
        session["mode"] = "track"
        reply = handle_track_grievance(session)
        #audio = text_to_speech(reply, language)
        return jsonify({"reply": reply})
 
    # =====================================================
    # DEVICE STATUS BUTTON
    # =====================================================
    if user_input == "SOLAR_PUMP_STATUS":
        reply = handle_device_status(farmer_context, language)
        #audio = text_to_speech(reply, language)
        return jsonify({"reply": reply})
 
    # =====================================================
    # SCHEME DETAILS FLOW
    # =====================================================
    scheme_options = [
        "Eligibility & Conditions",
        "Benefits",
        "How to Apply",
        "Contact Details",
        "Registration"
    ]
 
    if schema and user_input.strip() in scheme_options:
 
        # Reset grievance flow
        session["awaiting_confirmation"] = False
        session.pop("last_issue", None)
 
        reply = handle_scheme_query(schema, user_input.strip(), language)
        #audio = text_to_speech(reply, language)
 
        return jsonify({"reply": reply})
 
    # =====================================================
    # CONFIRMATION WORDS
    # =====================================================
    confirmation_words = [
        "yes", "ok", "okay", "sure",
        "haan", "ha", "haa", "हाँ",
        "হ্যাঁ"
    ]
 
    is_confirmation = any(word in lower_input for word in confirmation_words)
 
    # =====================================================
    # STEP 1: USER DESCRIBES ISSUE
    # =====================================================
    if schema and not session.get("awaiting_confirmation") and user_input.strip() not in scheme_options:
 
        session["last_issue"] = user_input
        session["awaiting_confirmation"] = True
 
       
 
        solution_prompt = f"""
You are JREDA Government AI Assistant.
 
User issue:
{user_input}
 
Provide:
1. Brief troubleshooting guidance.
2. Then politely ask if user wants to raise grievance.
 
Reply strictly in {language_instruction}.
If Santali is used, write ONLY in Romanized Santali using English letters.
 
No markdown.
No bold.
Professional tone.
"""
 
        reply = generate_response(solution_prompt)
        #audio = text_to_speech(reply, language)
        return jsonify({"reply": reply})
 
    # =====================================================
    # STEP 2: USER CONFIRMS → CREATE GRIEVANCE
    # =====================================================
    if session.get("awaiting_confirmation") and is_confirmation:
 
        issue_text = session.get("last_issue", "")
 
        # =========================================
        # STEP A: Generate LLM Issue Summary
        # =========================================
        summary_prompt = f"""
You are JREDA Government AI Assistant.
 
Summarize the user's issue professionally.
 
User Reported Issue:
{issue_text}
 
Rules:
- Do NOT add any heading.
- Do NOT write "Issue Summary:".
- Only return the explanation paragraph.
- Mention possible technical reason.
- Keep concise.
- Reply strictly in {language_instruction}.
- If Santali is used, write ONLY in Romanized Santali using English letters.
- Do NOT use Ol Chiki script.
- No markdown.
- No bold.
"""
 
        llm_summary = generate_response(summary_prompt)
 
        # =========================================
        # STEP B: Store grievance using LLM summary
        # =========================================
        record = store_grievance(
            {
                "Category": schema,
                "Issue Summary": llm_summary   # ✅ LLM GENERATED SUMMARY
            },
            farmer_context
        )
 
        session["awaiting_confirmation"] = False
        session.pop("last_issue", None)
 
 
        reply = f"""
        Grievance Confirmation
 
        Grievance ID: {record.get('grievance_id')}
        Mobile Number: {record.get('mobile_number')}
        Pump ID: {record.get('pump_id')}
        Category: {record.get('category')}
        Status: {record.get('current_status')}
        Created Date: {record.get('created_date')}
        Assigned Vendor: {record.get('assigned_vendor')}
        Expected Resolution: {record.get('expected_resolution_date')}
 
        Issue Summary:
        {llm_summary}
        """
 
        #audio = text_to_speech(reply, language)
 
        return jsonify({"reply": reply})
 
    # =====================================================
    # DEFAULT NORMAL RESPONSE
    # =====================================================
    general_prompt = f"""
    You are JREDA Government AI Assistant.
 
    Reply strictly in {language}.
    No markdown.
    Professional tone.
 
    IMPORTANT DOMAIN RULE:
 
    You are ONLY allowed to answer questions related to:
    - JREDA schemes
    - PM-KUSUM
    - Solar pumps
    - Grievance registration
    - Grievance tracking
    - Device status
    - Renewable energy programs under JREDA
 
    If the user asks anything unrelated to JREDA or solar services,
    politely refuse and guide them back to the available options.
 
    For unrelated questions, reply like:
    "This assistant is dedicated to JREDA solar services only. Please choose the available options only."
 
    User message:
    {user_input}
    """
 
    reply = generate_response(general_prompt)
    #audio = text_to_speech(reply, language)
 
    return jsonify({"reply": reply})
 