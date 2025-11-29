# voice_agent.py  (REPLACE YOUR OLD FILE WITH THIS)

import io
from openai import OpenAI
import streamlit as st

# Uses OPENAI_API_KEY from Streamlit secrets or env
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", None))

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Convert audio bytes (from st.audio_input) to text using
    the OpenAI Audio Transcriptions endpoint.
    """
    # Wrap raw bytes in a file-like object
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "input.wav"  # required for the SDK

    # gpt-4o-mini-transcribe is an official STT model
    # See docs: Audio & Speech → Transcriptions. 
    result = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_file,
    )
    # `text` holds the transcription string
    return result.text


def tts_speak(text: str) -> bytes:
    """
    Convert text to spoken audio using OpenAI Text-to-Speech.
    Returns raw bytes which you can pass to st.audio.
    """
    # gpt-4o-mini-tts is a TTS model; voice 'alloy' is supported. 
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    )

    # In the new Python SDK, .read() returns the audio bytes directly
    audio_bytes = response.read()
    return audio_bytes
