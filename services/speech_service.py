# import os
# import base64
# from dotenv import load_dotenv
# from google.genai import Client

# load_dotenv()

# API_KEY = os.getenv("GEMINI_API_KEY")

# if not API_KEY:
#     raise ValueError("GEMINI_API_KEY not found in .env")

# client = Client(api_key=API_KEY)


# # ============================================
# # 🎙 Speech to Text (Audio → Text)
# # ============================================

# def speech_to_text(audio_bytes, language="en-US"):

#     try:
#         response = client.models.generate_content(
#             model="models/gemini-2.5-flash-native-audio-latest",
#             contents=[
#                 {
#                     "role": "user",
#                     "parts": [
#                         {
#                             "mime_type": "audio/wav",
#                             "data": audio_bytes
#                         }
#                     ]
#                 }
#             ]
#         )

#         return response.text

#     except Exception as e:
#         print("STT Error:", e)
#         return "Speech recognition failed."


# # ============================================
# # 🔊 Text to Speech (Text → Audio)
# # ============================================

# def text_to_speech(text):

#     try:
#         response = client.models.generate_content_stream(
#             model="models/gemini-2.5-flash-native-audio-latest",
#             contents=[
#                 {
#                     "role": "user",
#                     "parts": [{"text": text}]
#                 }
#             ],
#             config={
#                 "response_mime_type": "audio/wav"
#             }
#         )

#         audio_bytes = b""

#         for chunk in response:
#             if chunk.candidates:
#                 parts = chunk.candidates[0].content.parts
#                 for part in parts:
#                     if hasattr(part, "data") and part.data:
#                         audio_bytes += part.data

#         if audio_bytes:
#             return base64.b64encode(audio_bytes).decode("utf-8")

#         print("No audio generated")
#         return None

#     except Exception as e:
#         print("TTS Error:", e)
#         return None

import base64
from gtts import gTTS
from io import BytesIO


# ============================================
# 🔊 TEXT TO SPEECH (TTS)
# ============================================

def text_to_speech(text, language="en"):

    try:
        tts = gTTS(text=text, lang=language)

        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)

        audio_bytes = audio_buffer.getvalue()

        return base64.b64encode(audio_bytes).decode("utf-8")

    except Exception as e:
        print("TTS Error:", e)
        return None