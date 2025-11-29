import os
import json
import streamlit as st

BASE = os.path.dirname(os.path.abspath(__file__))

def _find_config():
    candidates = [
        os.path.join(BASE, "chillers_config.json"),
        "chillers_config.json"
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    st.error("❌ chillers_config.json missing!")
    st.stop()

def load_chiller_config():
    path = _find_config()
    with open(path, "r") as f:
        return json.load(f)

def save_chiller_config(data):
    path = _find_config()
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
