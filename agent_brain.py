import json
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """
You are BMS Voice Agent for a Data Center.

Your responsibilities:
1. Speak like a professional BMS engineer.
2. Provide chiller, HVAC, AHU, PAHU, TFA insights.
3. Respond using short actionable sentences.
4. Never do real writeback. Only UI simulation.
5. If user says ON or OFF for a chiller, modify config.
6. If user asks for values, read from simulated API.
7. You can reason about Cooling, CRAC/PAHU/TFA units.
"""

def run_voice_agent(user_text, config, chiller_id=None):
    msg = f"""
User said: {user_text}
Selected chiller: {chiller_id}
Current config: {json.dumps(config)}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": msg},
        ],
    )

    return response.choices[0].message["content"]
