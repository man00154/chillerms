from openai import OpenAI
import re

client = OpenAI()

SYSTEM_PROMPT = """
You are BMS Voice Agent for a data center.
You control 30 chillers (CH-01 to CH-30) only in UI simulation mode.

Rules:
1. Never perform actual hardware writeback.
2. ON/OFF only updates JSON config.
3. Setpoints update JSON only.
4. Be short, professional, and precise.
5. You can extract chiller ID, ON/OFF commands, and setpoint values from user text.

Examples:
- "Turn on chiller 5" -> update chiller 5 to ON.
- "Switch off chiller 12" -> OFF
- "Set chiller 4 setpoint to 19.5" -> update setpoint
"""

def extract_chiller_id(text: str):
    """Extract CH number from user text."""
    m = re.findall(r'\b(\d{1,2})\b', text)
    if m:
        n = int(m[0])
        if 1 <= n <= 30:
            return n
    return None

def extract_setpoint(text: str):
    """Extract temperature setpoint."""
    m = re.search(r'(\d{2}\.?\d*)', text)
    if m:
        return float(m.group(1))
    return None


def run_agent(text, config):
    """
    Main BMS Voice Agent processor.
    Uses GPT only to generate natural responses,
    while the logic (ON/OFF/setpoint) is deterministic.
    """
    text = text.lower()

    # Detect chiller number
    ch_id = extract_chiller_id(text)

    # Detect ON/OFF
    is_on = any(x in text for x in ["turn on", "switch on", "start"])
    is_off = any(x in text for x in ["turn off", "switch off", "stop"])

    # Detect setpoint
    setp = None
    if "setpoint" in text or "set point" in text:
        setp = extract_setpoint(text)

    # If no chiller ID, send natural language response
    if ch_id is None:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ]
        )
        return resp.choices[0].message["content"], config

    # Get object
    ch = config["chillers"][ch_id - 1]  # zero-indexed

    # Process ON/OFF
    if is_on:
        ch["status"] = "ON"
    if is_off:
        ch["status"] = "OFF"

    # Process setpoint
    if setp is not None:
        ch["setpoint"] = setp

    # Update config
    config["chillers"][ch_id - 1] = ch

    # Natural agentic response
    response = f"Chiller {ch_id} updated. Status: {ch['status']}, Setpoint: {ch['setpoint']}°C"

    return response, config
