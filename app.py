import streamlit as st
from utils import load_json, save_json
from agent_brain import run_voice_agent
from layout_manager import show_layout
from simulator import simulate_on_off
from api_client import get_chiller_parameters
from hvac_manager import hvac_dashboard

st.set_page_config(layout="wide", page_title="BMS Voice Agent")

st.title("🔊 BMS Chiller + HVAC Voice Agent (30 Chillers)")

# Load config
cfg = load_json("chillers_config.json")

# Sidebar Navigation
st.sidebar.title("Navigation")
view = st.sidebar.selectbox("View", ["L1 Layout", "Cooling", "Chiller", "HVAC Dashboard"])

chiller_id = st.sidebar.number_input("Select Chiller", 1, 30, 1)

# Show Layout Images
show_layout(view)

# Chiller Dashboard
if view == "Chiller":
    st.subheader(f"Chiller {chiller_id} Parameters")
    data = get_chiller_parameters(chiller_id)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Supply Temp", data["supply_temp"])
    col2.metric("Return Temp", data["return_temp"])
    col3.metric("Power (kW)", data["power_kw"])
    col4.metric("Flow (m3/hr)", data["flow_m3hr"])

    # ON/OFF Simulation
    if st.button(f"Toggle CH{chiller_id} ON/OFF"):
        cfg["chillers"][str(chiller_id)] = simulate_on_off(cfg["chillers"][str(chiller_id)])
        save_json("chillers_config.json", cfg)
        st.success(f"Chiller {chiller_id} is now {cfg['chillers'][str(chiller_id)]}")

# HVAC Dashboard
if view == "HVAC Dashboard":
    hvac_dashboard()

# Voice Agent Input
st.subheader("🎤 Voice Assistant")
text = st.text_input("Say something to the BMS Agent...")
if st.button("Send to Voice Agent"):
    reply = run_voice_agent(text, cfg, chiller_id)
    st.success(reply)
