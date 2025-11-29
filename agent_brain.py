from openai import OpenAI
import re

client = OpenAI()

def extract_chiller_id(msg: str):
    nums = re.findall(r"\b(\d{1,2})\b", msg)
    if nums:
        n = int(nums[0])
        if 1 <= n <= 30:
            return n
    return None

def extract_setpoint(msg: str):
    m = re.search(r"(\d{2}\.?\d*)", msg)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None
    return None

def run_agent(message: str, config: dict):
    """
    Main agent that updates chiller config based on natural language.
    If it finds a chiller id and ON/OFF or setpoint command, it changes config.
    Otherwise, it just answers using the LLM.
    """
    msg = message.lower()

    ch_id = extract_chiller_id(msg)
    setp  = extract_setpoint(msg)

    is_on  = any(x in msg for x in ["turn on", "switch on", "start"])
    is_off = any(x in msg for x in ["turn off", "switch off", "stop"])

    # If it's clearly targeting a chiller
    if ch_id:
        ch = config["chillers"][ch_id - 1]

        if is_on:
            ch["status"] = "ON"
        if is_off:
            ch["status"] = "OFF"
        if setp is not None:
            ch["setpoint"] = setp

        config["chillers"][ch_id - 1] = ch
        reply = f"CH-{ch_id:02d} updated → Status: {ch['status']}, Setpoint: {ch['setpoint']}°C"
        return reply, config

    # Otherwise: just chat using GPT
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}],
    )
    reply = resp.choices[0].message["content"]
    return reply, config
