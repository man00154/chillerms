import streamlit as st
from utils import load_chiller_config, save_chiller_config
from simulator import simulate_chiller_readings, simulate_toggle_status
from layout_manager import show_layout
from hvac_manager import hvac_dashboard
from agent_brain import run_agent

st.set_page_config(page_title="BMS Voice Agent – Manish Singh - Chiller Dashboard", layout="wide")

# ----------------------------------------------------
# Load config (30 chillers)
# ----------------------------------------------------
config = load_chiller_config()

# ----------------------------------------------------
# Sidebar Navigation
# ----------------------------------------------------
st.sidebar.title("Navigation")
view = st.sidebar.selectbox(
    "Select View",
    [
        "L1 Layout",
        "Cooling Layout",
        "Chiller Dashboard",
        "Single Chiller",
        "HVAC Dashboard",
        "Voice Agent",
    ]
)

selected_chiller = st.sidebar.number_input("Chiller Number", 1, 30, 1)

# ----------------------------------------------------
# Show Layout Views (L1 Layout, Cooling)
# ----------------------------------------------------
if view in ["L1 Layout", "Cooling Layout"]:
    show_layout(view)

# ----------------------------------------------------
# CHILLER DASHBOARD — 30 chillers in 3×10 GRID
# ----------------------------------------------------
if view == "Chiller Dashboard":
    st.title("MUM-03-T5-L1 | CHILLER DASHBOARD")

    NUM_CHILLERS = 30
    CHILLERS_PER_ROW = 10

    # ---- Grid (3 Rows × 10 Columns) ----
    for row_start in range(1, NUM_CHILLERS + 1, CHILLERS_PER_ROW):

        cols = st.columns(CHILLERS_PER_ROW)

        for offset in range(CHILLERS_PER_ROW):

            ch_id = row_start + offset
            if ch_id > NUM_CHILLERS:
                break

            # Column for individual chiller
            col = cols[offset]

            # Fetch config object
            ch = config["chillers"][ch_id - 1]

            # Simulation
            sim = simulate_chiller_readings(ch["setpoint"])

            # --------------------------------------------------------
            # UI BOX (Matches screenshot)
            # --------------------------------------------------------

            # Blue header bar
            col.markdown(
                f"""
                <div style='background-color:#004b80;
                            color:white;text-align:center;
                            padding:4px;font-weight:bold;
                            font-size:13px;'>
                    {ch['name']}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ON/OFF bar
            color = "#00aa00" if ch["status"] == "ON" else "#aa0000"
            col.markdown(
                f"""
                <div style='background-color:{color};
                            color:white;text-align:center;
                            padding:4px;font-size:12px;'>
                    STATUS: {ch['status']}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Dark parameter rectangle
            col.markdown(
                f"""
                <div style='background-color:#111;padding:6px;
                            font-size:11px;line-height:1.4;
                            color:#ddd;'>

                    <b>Setpoint (°C):</b> {ch['setpoint']}<br>
                    <b>Supply Temp (°C):</b> {sim['supply_temp']}<br>
                    <b>Unit Inlet Temp (°C):</b> {sim['inlet_temp']}<br>
                    <b>Unit Outlet Temp (°C):</b> {sim['outlet_temp']}<br>
                    <b>Ambient Temp (°C):</b> {sim['ambient_temp']}<br>
                    <b>Comp-1 Load (%):</b> {sim['comp1']}<br>
                    <b>Comp-2 Load (%):</b> {sim['comp2']}<br>
                    <b>Power (kW):</b> {sim['power_kw']}<br>
                    <b>Water Flow (m³/hr):</b> {sim['water_flow']}<br>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # --------------------------------------------------------
            # Controls (Toggle + Setpoint)
            # --------------------------------------------------------

            # Toggle ON/OFF
            if col.button(f"Toggle {ch['name']}", key=f"t{ch_id}"):
                ch["status"] = simulate_toggle_status(ch["status"])
                config["chillers"][ch_id - 1] = ch
                save_chiller_config(config)
                st.experimental_rerun()

            # Setpoint input
            new_sp = col.number_input(
                f"Setpoint {ch['name']}",
                16.0, 26.0, ch["setpoint"], 0.1,
                key=f"sp{ch_id}"
            )
            if new_sp != ch["setpoint"]:
                ch["setpoint"] = new_sp
                config["chillers"][ch_id - 1] = ch
                save_chiller_config(config)

    # ----------------------------------------------------
    # Bottom Alarm/Event Strip
    # ----------------------------------------------------
    st.markdown("---")
    st.subheader("⚠️ ALARMS / EVENTS (Simulated)")

    alarms = [
        {"time": "29-Nov-25 12:23 PM", "msg": "T5-LEVEL-1-PUMP-UPS-L1-B1 FLOAT-CHARGE ALARM"},
        {"time": "29-Nov-25 10:15 AM", "msg": "PAHU-A2 UNIT STATUS OFF"},
        {"time": "28-Nov-25 02:48 PM", "msg": "DUCT-AFET-DET-011 TROUBLE"},
        {"time": "28-Nov-25 02:45 PM", "msg": "HVAC ROOM BM-002 DISABLE"},
    ]

    for a in alarms:
        st.markdown(
            f"""
            <div style='background:#000;color:#f5f5f5;
                        padding:6px;border-bottom:1px solid #333;
                        font-size:12px;'>
                <span style='color:#ffcc66;'>{a['time']}</span>
                &nbsp;&nbsp; {a['msg']}
            </div>
            """,
            unsafe_allow_html=True,
        )

# ----------------------------------------------------
# SINGLE CHILLER VIEW
# ----------------------------------------------------
if view == "Single Chiller":
    st.header(f"Single Chiller – CH-{selected_chiller:02d}")

    ch = config["chillers"][selected_chiller - 1]
    sim = simulate_chiller_readings(ch["setpoint"])

    st.write("### Live Parameters")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Supply Temp", sim["supply_temp"])
    col2.metric("Inlet Temp", sim["inlet_temp"])
    col3.metric("Outlet Temp", sim["outlet_temp"])
    col4.metric("Ambient Temp", sim["ambient_temp"])

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Comp-1 Load", sim["comp1"])
    col6.metric("Comp-2 Load", sim["comp2"])
    col7.metric("Power (kW)", sim["power_kw"])
    col8.metric("Water Flow", sim["water_flow"])

    if st.button("Toggle ON/OFF"):
        ch["status"] = simulate_toggle_status(ch["status"])
        config["chillers"][selected_chiller - 1] = ch
        save_chiller_config(config)
        st.experimental_rerun()

# ----------------------------------------------------
# HVAC Dashboard
# ----------------------------------------------------
if view == "HVAC Dashboard":
    hvac_dashboard()

# ----------------------------------------------------
# Voice Agent (text-based proxy)
# ----------------------------------------------------
if view == "Voice Agent":
    st.header("🎤 BMS Voice Agent (Text Proxy)")

    user_message = st.text_input("Ask something (e.g., 'Turn ON chiller 5'):")

    if st.button("Ask"):
        if user_message.strip():
            reply, updated_config = run_agent(user_message, config)
            config = updated_config
            save_chiller_config(config)
            st.success(reply)
        else:
            st.info("Enter a command to continue.")
