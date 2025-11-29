import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def start_voice():
    return await client.realtime.sessions.create(
        model="gpt-4o-realtime-preview",
        voice="alloy",
        modalities=["audio", "text", "tool"]
    )
