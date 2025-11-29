# voice_agent.py
import streamlit as st
from openai import OpenAI
import base64

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def transcribe_audio(audio_bytes):
    """Convert mic audio → text"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini-tts",
        messages=[{"role": "user", "content": "transcribe this"}],
        audio={"input": audio_bytes, "format": "wav"}
    )
    return resp.choices[0].message["content"]


def tts_speak(text):
    """Convert text → spoken audio"""
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    audio_base64 = speech.audio
    audio_bytes = base64.b64decode(audio_base64)
    return audio_bytes
