import io
import base64
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Convert uploaded/mic audio bytes to text using OpenAI Audio API.
    """
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "input.wav"

    transcript = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_file,
    )
    # 'text' attribute holds the transcription
    return transcript.text

def tts_speak(text: str) -> bytes:
    """
    Convert text to spoken audio bytes using OpenAI Audio TTS.
    """
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    )
    # For the Python SDK, use read() to get raw bytes
    return response.read()
