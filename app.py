import streamlit as st
from utils import load_json, save_json
from agent_brain import run_voice_agent
from layout_manager import show_layout
from simulator import simulate_on_off
from api_client import get_chiller_parameters
from hvac_manager import hvac_dashboard

st.set_page_config(layout="wide", page_title="BMS Voice Agent – MANISH SINGH - Chiller Dashboard")

st.title("MUM-03-T5-L1  |  CHILLER_DASHBOARD  |  BMS Voice Agent")

# ----------------------------
# Load & cache configuration
# ----------------------------
cfg = load_json("chillers_config.json")

# ----------------------------
# Sidebar navigation
# ----------------------------
st.sidebar.title("Navigation")

view = st.sidebar.selectbox(
    "View",
    ["L1 Layout", "Cooling Layout", "Chiller Dashboard", "Single Chiller", "HVAC Dashboard"],
)

selected_chiller = st.sidebar.number_input("Select Chiller (for single view)", 1, 30, 1)

# ----------------------------
# L1 Layout / Cooling image views
# ----------------------------
if view in ["L1 Layout", "Cooling Layout"]:
    show_layout(view)

# ----------------------------
# CHILLER DASHBOARD (grid like your screenshot)
# ----------------------------
if view == "Chiller Dashboard":
    st.subheader("Chiller Grid – Live Parameters")

    # two main columns: left = chiller grid, right = “gauges”
    grid_col, gauge_col = st.columns([4, 1])

    # ----- LEFT: chiller grid -----
    with grid_col:
        # We will show 20 chillers in 2 rows x 10 columns (like screenshot)
        NUM_CHILLERS = 20
        CHILLERS_PER_ROW = 10

        for row_start in range(1, NUM_CHILLERS + 1, CHILLERS_PER_ROW):
            cols = st.columns(CHILLERS_PER_ROW)
            for offset in range(CHILLERS_PER_ROW):
                ch_id = row_start + offset
                if ch_id > NUM_CHILLERS:
                    break

                col = cols[offset]
                data = get_chiller_parameters(ch_id)
                status = cfg["chillers"][str(ch_id)]

                # header – chiller name
                col.markdown(
                    f"<div style='background-color:#004b80;color:white;font-weight:bold;"
                    f"text-align:center;padding:4px;'>T5-CHILLER-{ch_id:02d}</div>",
                    unsafe_allow_html=True,
                )

                # on/off bar
                bg = "#00aa00" if status == "ON" else "#aa0000"
                col.markdown(
                    f"<div style='background-color:{bg};color:white;text-align:center;"
                    f"padding:4px;m
