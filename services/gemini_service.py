# import os
# from dotenv import load_dotenv
# from google.genai import Client
# from services.web_scraper_service import fetch_website_content
# from services.pdf_service import extract_pdf_text

# load_dotenv()

# client = Client(api_key=os.getenv("GEMINI_API_KEY"))

# PDF_TEXT = extract_pdf_text("Data/PM_KUSUM_details_hindi.pdf")

# def build_prompt(user_input, language, verified, farmer_context=None, schema=None, last_grievance=None):

#     website_content = fetch_website_content()

#     return f"""
# You are a JREDA Government AI Assistant.

# Reply strictly in {language}.
# Keep responses short and professional.
# Plain text only.

# FLOW:

# 1. If user explains issue:
#    - Provide short solution.
#    - Ask if they want to raise grievance.

# 2. If user confirms:
# Return ONLY:

# RAISE_GRIEVANCE_APPROVED
# Category: {schema}
# Issue Summary: short summary of user's issue.

# 3. If user asks about previously created grievance:
# Explain clearly using Previous Grievance data below.

# Previous Grievance:
# {last_grievance if last_grievance else "None"}

# IMPORTANT:
# - Issue Summary must reflect user's complaint.
# - Do not infer hardware faults.
# - Backend generates ticket details.

# User Query:
# {user_input}
# """

# def generate_response(prompt):
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     text = response.text.strip()

#     # Remove markdown symbols if model adds them
#     text = text.replace("**", "")
#     text = text.replace("*", "")

#     return text

import os
from dotenv import load_dotenv
from google.genai import Client
from services.web_scraper_service import fetch_website_content
from services.pdf_service import extract_pdf_text

load_dotenv()

client = Client(api_key=os.getenv("GEMINI_API_KEY"))

PDF_TEXT = extract_pdf_text("Data/PM_KUSUM_details_hindi.pdf")


# ============================================
# 🔒 STRONG LANGUAGE LOCK
# ============================================

def language_lock(language):
    return f"""
LANGUAGE POLICY (MANDATORY):

You MUST reply ONLY in {language}.

Language rules:
- English → English only
- Hindi → Hindi script only
- Bengali → Bengali script only
- Santali → Romanized Santali (English letters)

If official content is in Hindi and user selected Bengali or English,
you MUST translate the content fully into {language}.

Do NOT mix languages.
Do NOT default to Hindi.
Do NOT include Hindi words unless language is Hindi.

Plain text only.
No markdown.
No bold formatting.
Professional government tone.
"""


# ============================================
# 🔧 BUILD PROMPT
# ============================================

def build_prompt(user_input, language, verified, farmer_context=None, schema=None, last_grievance=None):

    website_content = fetch_website_content()

    return f"""
You are a JREDA Government AI Assistant.

{language_lock(language)}

FLOW:

1. If user explains issue:
   - Provide short troubleshooting solution.
   - Ask politely if they want to raise grievance.

2. If user confirms:
Return ONLY:

RAISE_GRIEVANCE_APPROVED
Category: {schema}
Issue Summary: short summary of user's exact complaint.

3. If user asks about previously created grievance:
Explain clearly using Previous Grievance data below.

Previous Grievance:
{last_grievance if last_grievance else "None"}

IMPORTANT RULES:
- Issue Summary must reflect user's complaint exactly.
- Do NOT invent technical faults.
- Do NOT generate scheme-level delays.
- Backend generates ticket details.

User Query:
{user_input}
"""


# ============================================
# 🤖 GENERATE RESPONSE
# ============================================

def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Safety cleanup
    text = text.replace("**", "")
    text = text.replace("*", "")

    return text