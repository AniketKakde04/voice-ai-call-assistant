import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def transcribe_and_respond(audio_bytes: bytes) -> str:
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    prompt = "You are a helpful AI assistant. Understand what the caller is saying and respond helpfully in English. Be polite and brief."

    response = model.generate_content([
        prompt,
        {
            "mime_type": "audio/wav",  # Twilio records in WAV format
            "data": audio_bytes
        }
    ])

    return response.text.strip()
