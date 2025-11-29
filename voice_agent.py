from openai import OpenAI
import streamlit as st
import base64

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def transcribe_audio(audio_bytes):
    out = client.audio.transcriptions.create(
        model="gpt-4o-mini-tts",
        file=audio_bytes,
        response_format="text"
    )
    return out

def tts_speak(text):
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    audio = base64.b64decode(response.audio)
    return audio
