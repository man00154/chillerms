from langgraph.graph import StateGraph, END
from chiller_api import get_chiller_live
from hvac_api import get_ahu_live, get_pahu_live, get_tfa_live
from utils import load_json, save_json

def process_user(state):
    text = state["user"]

    if "chiller" in text.lower() and ("on" in text.lower() or "off" in text.lower()):
        num = int(''.join([c for c in text if c.isdigit()]))
        cfg = load_json("config/chillers_config.json")
        if "on" in text.lower():
            cfg["chillers"][str(num)]["status"] = "ON"
        else:
            cfg["chillers"][str(num)]["status"] = "OFF"
        save_json("config/chillers_config.json", cfg)
        return {"assistant": f"Chiller {num} turned {cfg['chillers'][str(num)]['status']}"}

    if "ahu" in text.lower():
        return {"assistant": str(get_ahu_live(1))}

    if "pahu" in text.lower():
        return {"assistant": str(get_pahu_live(1))}

    if "tfa" in text.lower():
        return {"assistant": str(get_tfa_live(1))}

    return {"assistant": "Command received"}

def build_agent():
    g = StateGraph(dict)
    g.add_node("process", process_user)
    g.set_entry_point("process")
    g.add_edge("process", END)
    return g.compile()
