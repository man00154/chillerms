import streamlit as st

from utils import load_chiller_config, save_chiller_config
from simulator import simulate_chiller_readings, simulate_toggle_status
from hvac_manager import hvac_dashboard
from agent_brain import run_agent
from voice_agent import transcribe_audio, tts_speak

# -------------------------------------------------------
# Page config
# -------------------------------------------------------
st.set_page_config(
    page_title="BMS AI Voice Agent – Chiller Dashboard",
    layout="wide"
)

# Load configuration (30 chillers)
config = load_chiller_config()

st.title("🏭 DATA CENTER – BMS CHILLER DASHBOARD MANISH SINGH (Single Page, Simulated)")

# -------------------------------------------------------
# SECTION 1 — 30 CHILLER GRID (3 × 10)
# -------------------------------------------------------
st.header("Chiller Plant – 30 Units (3 × 10 Grid)")

NUM_CHILLERS = 30
CHILLERS_PER_ROW = 10

for row in range(3):
    cols = st.columns(CHILLERS_PER_ROW)
    for col_idx in range(CHILLERS_PER_ROW):
        ch_id = row * CHILLERS_PER_ROW + col_idx + 1
        ch = config["chillers"][ch_id - 1]
        sim = simulate_chiller_readings(ch["setpoint"])
        col = cols[col_idx]

        # Blue header
        col.markdown(
            f"<div style='background:#004b80;color:white;text-align:center;"
            f"padding:4px;font-size:12px;font-weight:bold;'>CH-{ch_id:02d}</div>",
            unsafe_allow_html=True,
        )

        # Status bar
        color = "#00aa00" if ch["status"] == "ON" else "#aa0000"
        col.markdown(
            f"<div style='background:{color};color:white;text-align:center;"
            f"padding:4px;font-size:12px;'>STATUS: {ch['status']}</div>",
            unsafe_allow_html=True,
        )

        # Data panel
        col.markdown(
            f"""
            <div style='background:#111;padding:6px;font-size:11px;color:#ddd;'>
                <b>Setpoint:</b> {ch['setpoint']}°C<br>
                <b>Supply:</b> {sim['supply_temp']}°C<br>
                <b>Inlet:</b> {sim['inlet_temp']}°C<br>
                <b>Outlet:</b> {sim['outlet_temp']}°C<br>
                <b>Ambient:</b> {sim['ambient_temp']}°C<br>
                <b>Comp-1:</b> {sim['comp1']}%<br>
                <b>Comp-2:</b> {sim['comp2']}%<br>
                <b>Power:</b> {sim['power_kw']} kW<br>
                <b>Flow:</b> {sim['water_flow']} m³/hr<br>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Toggle button (using st.rerun)
        if col.button(f"Toggle CH-{ch_id}", key=f"toggle_{ch_id}"):
            ch["status"] = simulate_toggle_status(ch["status"])
            config["chillers"][ch_id - 1] = ch
            save_chiller_config(config)
            st.rerun()

        # Setpoint input
        new_sp = col.number_input(
            f"SP CH-{ch_id}", 16.0, 26.0, ch["setpoint"], 0.1,
            key=f"sp_{ch_id}"
        )
        if new_sp != ch["setpoint"]:
            ch["setpoint"] = new_sp
            config["chillers"][ch_id - 1] = ch
            save_chiller_config(config)

# -------------------------------------------------------
# SECTION 2 — HVAC
# -------------------------------------------------------
st.markdown("---")
hvac_dashboard()

# -------------------------------------------------------
# SECTION 3 — ALARMS (Simulated)
# -------------------------------------------------------
st.markdown("---")
st.header("⚠️ Active Alarms (Simulated)")
alarms = [
    "T5-L1 Pump UPS Float-Charge Alarm",
    "PAHU-A2 Unit Status OFF",
    "DUCT-AFET-DET-011 Trouble",
]
for a in alarms:
    st.markdown(f"- 🔶 **{a}**")

# -------------------------------------------------------
# SECTION 4 — VOICE TO VOICE AGENT
# -------------------------------------------------------
st.markdown("---")
st.header("🎤 Voice to Voice – BMS AI Agent")

audio = st.audio_input("Speak a command (e.g., 'Turn on chiller 5', 'Set chiller 7 setpoint to 20.5')")
if audio is not None:
    try:
        st.info("Transcribing your voice command...")
        # Read raw bytes from the UploadedFile
        raw_bytes = audio.read()

        # 1) Speech → Text
        text = transcribe_audio(raw_bytes)
        st.write(f"🗣 You said: **{text}**")

        # 2) Use agent logic to interpret and update chillers
        reply, updated_config = run_agent(text, config)
        config = updated_config
        save_chiller_config(config)

        st.success(reply)

        # 3) Text → Speech
        st.info("Generating spoken response...")
        audio_out = tts_speak(reply)
        st.audio(audio_out, format="audio/wav")

    except Exception as e:
        st.error(f"Voice agent error: {e}")
