# voice_agent.py

import io
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", None))

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Convert audio bytes (from st.audio_input or file_uploader) to text
    using the OpenAI Audio Transcriptions endpoint.
    """
    if not audio_bytes:
        return ""

    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "input.wav"  # required by SDK

    result = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_file,
    )
    return result.text or ""


def tts_speak(text: str) -> bytes:
    """
    Convert text to spoken audio using OpenAI Text-to-Speech.
    Returns raw bytes which you can pass to st.audio.
    """
    if not text:
        return b""

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    )
    return response.read()
