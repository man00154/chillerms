import asyncio
import streamlit as st
from openai import AsyncOpenAI

# Load key safely from Streamlit secrets
API_KEY = st.secrets["OPENAI_API_KEY"]

client = AsyncOpenAI(api_key=API_KEY)

async def start_voice():
    session = await client.realtime.sessions.create(
        model="gpt-4o-realtime-preview",
        voice="alloy",
        modalities=["audio", "text", "tool"]
    )
    return session
