# from services.pdf_service import extract_pdf_text
# from services.web_scraper_service import fetch_website_content
# from services.gemini_service import generate_response

# # Load once (important for performance)
# PDF_TEXT = extract_pdf_text("Data/PM_KUSUM_details_hindi.pdf")
# WEBSITE_TEXT = fetch_website_content()


# def handle_scheme_query(schema, user_option, language):

#     # -------------------------------------------------
#     # 🔥 LIMIT CONTENT SIZE (PREVENT TOKEN OVERFLOW)
#     # -------------------------------------------------

#     website_content = WEBSITE_TEXT[:6000]

#     if schema == "PM-KUSUM Scheme (C)":
#         pdf_content = PDF_TEXT[:4000]

#         knowledge_source = f"""
# OFFICIAL WEBSITE CONTENT:
# {website_content}

# OFFICIAL PM-KUSUM PDF CONTENT:
# {pdf_content}
# """
#     else:
#         knowledge_source = f"""
# OFFICIAL WEBSITE CONTENT:
# {website_content}
# """

#     # -------------------------------------------------
#     # 🔐 STRICT GOVERNMENT PROMPT
#     # -------------------------------------------------

#     prompt = f"""
# You are JREDA Government AI Assistant.

# Reply strictly in {language}.
# Use a formal and professional government tone.

# Formatting Rules:
# - Do NOT use markdown symbols like ** or *.
# - Use proper headings in plain text.
# - Use numbered points (1., 2., 3.) where applicable.
# - Use short paragraphs.
# - Leave one blank line between sections.
# - Make headings clearly written in Title Case.

# Answer only from the official content provided below.
# Do NOT invent information.
# If information is not available, say:
# "The requested information is not available in the official records."

# Scheme: {schema}
# User Request: {user_option}

# ====================================================
# OFFICIAL CONTENT STARTS
# ====================================================

# {knowledge_source}

# ====================================================
# OFFICIAL CONTENT ENDS
# ====================================================
# """

#     try:
#         response = generate_response(prompt)
#         return response.strip() if response else "No response generated."
#     except Exception as e:
#         print("Scheme LLM Error:", str(e))
#         return "Unable to fetch scheme details at the moment. Please try again later."

from services.pdf_service import extract_pdf_text
from services.web_scraper_service import fetch_website_content
from services.gemini_service import generate_response
import os
 
# ============================================
# LOAD OFFICIAL CONTENT (SAFE PATH)
# ============================================
 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = os.path.join(BASE_DIR, "Data", "PM_KUSUM_details_hindi.pdf")
 
PDF_TEXT = extract_pdf_text(PDF_PATH)
WEBSITE_TEXT = fetch_website_content()
 
 
def handle_scheme_query(schema, user_option, language):
 
    # ============================================
    # LIMIT CONTENT SIZE (PREVENT TOKEN OVERFLOW)
    # ============================================
 
    website_content = WEBSITE_TEXT[:6000]
    pdf_content = PDF_TEXT[:4000]
 
    if schema == "PM-KUSUM Scheme (C)":
        knowledge_source = f"""
OFFICIAL WEBSITE CONTENT:
{website_content}
 
OFFICIAL PM-KUSUM PDF CONTENT:
{pdf_content}
"""
    else:
        knowledge_source = f"""
OFFICIAL WEBSITE CONTENT:
{website_content}
"""
 
    # ============================================
    # STRONG LANGUAGE ENFORCEMENT PROMPT
    # ============================================
 
    prompt = f"""
You are JREDA Government AI Assistant.
 
CRITICAL LANGUAGE RULE:
You MUST respond ONLY in {language}.
Do NOT mix languages.
Do NOT include Hindi unless selected language is Hindi.
Do NOT include English unless selected language is English.
If the official content is in Hindi, you must fully translate it into {language} before responding.
Never copy Hindi text if {language} is Bengali or English.
 
LANGUAGE BEHAVIOR RULES:
- If language is Bengali → Respond fully in Bengali script.
- If language is Hindi → Respond fully in Hindi script.
- If language is Santali → Respond in Romanized Santali.
- If language is English → Respond fully in English.
 
Formatting Rules:
- Do NOT use markdown symbols like ** or *
- Use proper plain headings
- Use numbered points where applicable
- Keep paragraphs short
- Maintain formal government tone
 
Answer ONLY using the official content provided below.
Do NOT invent information.
If information is not available, say:
"The requested information is not available in the official records."
 
Scheme: {schema}
User Request: {user_option}
 
====================================================
OFFICIAL CONTENT STARTS
====================================================
 
{knowledge_source}
 
====================================================
OFFICIAL CONTENT ENDS
====================================================
"""
 
    try:
        response = generate_response(prompt)
        return response.strip() if response else "No response generated."
    except Exception as e:
        print("Scheme LLM Error:", str(e))
        return "Unable to fetch scheme details at the moment. Please try again later."