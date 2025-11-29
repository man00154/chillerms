from openai import OpenAI
import re

client = OpenAI()

def extract_chiller_id(msg):
    nums = re.findall(r"\b(\d{1,2})\b", msg)
    if nums:
        n = int(nums[0])
        if 1 <= n <= 30:
            return n
    return None

def extract_setpoint(msg):
    m = re.search(r"(\d{2}\.?\d*)", msg)
    if m:
        return float(m.group(1))
    return None

def run_agent(message, config):
    msg = message.lower()

    ch_id = extract_chiller_id(msg)
    setp  = extract_setpoint(msg)

    is_on  = any(x in msg for x in ["turn on", "switch on", "start"])
    is_off = any(x in msg for x in ["turn off", "switch off", "stop"])

    if ch_id:
        ch = config["chillers"][ch_id - 1]

        if is_on:
            ch["status"] = "ON"
        if is_off:
            ch["status"] = "OFF"
        if setp:
            ch["setpoint"] = setp

        config["chillers"][ch_id - 1] = ch
        reply = f"CH-{ch_id:02d} updated → Status: {ch['status']} | SP: {ch['setpoint']}°C"
        return reply, config

    reply = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}]
    ).choices[0].message["content"]

    return reply, config
