import streamlit as st
import asyncio
from voice_realtime import start_voice
from agent_graph import build_agent
from utils import load_json, save_json
from layout_manager import show_layout
from chiller_api import get_chiller_live
from hvac_api import get_ahu_live
from data_simulator import simulate_chiller

st.set_page_config(layout="wide", page_title="BMS Voice Agent")

st.title("🎙️ BMS Voice Agent – Chiller + HVAC + TFA + PAHU")

agent = build_agent()

layout = st.sidebar.selectbox("Dashboard", ["Cooling", "Chiller", "L1 Layout"])
show_layout(layout)

st.sidebar.header("Chiller Control")
ch = st.sidebar.selectbox("Select Chiller (1–30)", list(range(1,31)))

cfg = load_json("config/chillers_config.json")

if st.sidebar.button("Turn ON"):
    cfg["chillers"][str(ch)]["status"] = "ON"
    save_json("config/chillers_config.json", cfg)

if st.sidebar.button("Turn OFF"):
    cfg["chillers"][str(ch)]["status"] = "OFF"
    save_json("config/chillers_config.json", cfg)

st.sidebar.write("Status:", cfg["chillers"][str(ch)]["status"])

st.header("Live Chiller Telemetry")
live = get_chiller_live(ch)
st.json(live)

st.header("Simulation Data")
sim = simulate_chiller(ch)
st.json(sim)

st.header("🎤 Speak to BMS Voice Agent")
voice = st.file_uploader("Upload voice (wav/mp3)", type=["wav", "mp3"])

if voice:
    user_text = "Turn on chiller " + str(ch)  # placeholder for speech_recognition pipeline
    out = agent({"user": user_text})
    st.write("🗣️ Agent:", out["assistant"])
