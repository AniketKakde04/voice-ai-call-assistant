from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Record, Say
from dotenv import load_dotenv
from gemini_utils import transcribe_and_respond
from twilio_utils import download_audio_file
import os

app = Flask(__name__)
load_dotenv()

@app.route("/voice", methods=["POST"])
def voice_webhook():
    """Initial voice route - record user's speech."""
    resp = VoiceResponse()
    resp.say("Hello! Please say something after the beep. I will respond intelligently.")
    resp.record(
        action="/handle-recording",
        max_length=10,
        play_beep=True,
        timeout=3
    )
    return Response(str(resp), mimetype="application/xml")

@app.route("/handle-recording", methods=["POST"])
def handle_recording():
    """Handles the recorded audio and responds via TTS."""
    recording_url = request.form.get("RecordingUrl")  # This is a WAV file URL
    if not recording_url:
        resp = VoiceResponse()
        resp.say("Sorry, I couldn't get your message.")
        return Response(str(resp), mimetype="application/xml")

    try:
        # Download the WAV audio file from Twilio
        audio_bytes = download_audio_file(recording_url + ".wav")

        # Use Gemini to generate an intelligent reply
        reply = transcribe_and_respond(audio_bytes)

        # Convert text to speech using <Say>
        resp = VoiceResponse()
        resp.say(reply, voice="Polly.Aditi", language="en-IN")  # use Twilio-compatible voices
        return Response(str(resp), mimetype="application/xml")

    except Exception as e:
        print("Error:", e)
        resp = VoiceResponse()
        resp.say("Sorry, I couldn't process your message.")
        return Response(str(resp), mimetype="application/xml")
