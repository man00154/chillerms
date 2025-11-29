import streamlit as st
from utils import load_chiller_config, save_chiller_config
from simulator import simulate_chiller_readings, simulate_toggle_status
from layout_manager import show_layout
from hvac_manager import hvac_dashboard
from agent_brain import run_agent
from image_click import get_chiller_from_click
from voice_agent import transcribe_audio, tts_speak

st.set_page_config(page_title="BMS Voice Agent – Manish Singh -  Chiller Dashboard", layout="wide")
config = load_chiller_config()


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
st.sidebar.title("Navigation")
view = st.sidebar.selectbox(
    "Select View",
    ["L1 Layout", "Cooling Layout", "Chiller Dashboard", "Single Chiller", "HVAC Dashboard", "Voice-To-Voice"]
)
selected_chiller = st.sidebar.number_input("Selected Chiller", 1, 30, 1)


# ---------------------------------------------------------
# L1 LAYOUT CLICKABLE (X,Y detection)
# ---------------------------------------------------------
if view == "L1 Layout":
    st.subheader("Clickable L1 Layout (Select Chiller by clicking image below)")

    click = st.image("l1 chiller layout.png", use_column_width=True)

    # Streamlit's click detector
    if "clicked" not in st.session_state:
        st.session_state.clicked = None

    event = st.session_state.get("clicked")

    uploaded_event = st.experimental_get_query_params()

    # Use JavaScript hack to capture X,Y
    click_js = """
        <script>
        const img = document.querySelector('img[alt="l1 chiller layout.png"]');
        img.addEventListener('click', (e) => {
            const rect = e.target.getBoundingClientRect();
            const x = e.clientX - rect.left; 
            const y = e.clientY - rect.top;
            const py = document.createElement('p');
            py.id = "xycoord";
            py.innerText = `${x},${y}`;
            document.body.append(py);
        });
        </script>
    """
    st.markdown(click_js, unsafe_allow_html=True)

    # User manually pastes coordinates into textbox
    xy = st.text_input("Paste X,Y from click →")

    if xy:
        try:
            x, y = xy.split(',')
            x = float(x)
            y = float(y)
            detected = get_chiller_from_click(x, y)
            if detected:
                st.success(f"Selected Chiller → CH-{detected:02d}")
                selected_chiller = detected
        except:
            st.error("Invalid XY format.")


# ---------------------------------------------------------
# CHILLER DASHBOARD (30 CHILLERS, identical to screenshot)
# ---------------------------------------------------------
if view == "Chiller Dashboard":
    st.title("CHILLER DASHBOARD – 30 Units (3×10 Grid)")

    NUM_CHILLERS = 30
    PER_ROW = 10

    for row in range(3):
        cols = st.columns(PER_ROW)
        for col_idx in range(PER_ROW):

            ch_id = row * 10 + col_idx + 1
            c = cols[col_idx]

            ch = config["chillers"][ch_id - 1]
            sim = simulate_chiller_readings(ch["setpoint"])

            # Blue header
            c.markdown(
                f"<div style='background:#004b80;color:white;text-align:center;"
                f"padding:4px;font-size:12px;font-weight:bold;'>CH-{ch_id:02d}</div>",
                unsafe_allow_html=True,
            )

            # Status bar
            color = "#00aa00" if ch["status"] == "ON" else "#aa0000"
            c.markdown(
                f"<div style='background:{color};color:white;text-align:center;"
                f"padding:4px;font-size:12px;'>STATUS: {ch['status']}</div>",
                unsafe_allow_html=True,
            )

            # Black data box
            c.markdown(
                f"""
                <div style='background:#111;padding:6px;font-size:11px;line-height:1.4;color:#ddd;'>
                    <b>Setpoint (°C):</b> {ch['setpoint']}<br>
                    <b>Supply Temp:</b> {sim['supply_temp']}<br>
                    <b>Inlet Temp:</b> {sim['inlet_temp']}<br>
                    <b>Outlet Temp:</b> {sim['outlet_temp']}<br>
                    <b>Ambient Temp:</b> {sim['ambient_temp']}<br>
                    <b>Comp-1 Load:</b> {sim['comp1']}<br>
                    <b>Comp-2 Load:</b> {sim['comp2']}<br>
                    <b>Power (kW):</b> {sim['power_kw']}<br>
                    <b>Water Flow:</b> {sim['water_flow']}<br>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Toggle ON/OFF
            if c.button(f"Toggle CH-{ch_id}", key=f"tog{ch_id}"):
                ch["status"] = simulate_toggle_status(ch["status"])
                config["chillers"][ch_id - 1] = ch
                save_chiller_config(config)
                st.experimental_rerun()

            # Setpoint field
            new_sp = c.number_input(
                f"SP CH-{ch_id}",
                16.0, 26.0, ch["setpoint"], 0.1,
                key=f"sp{ch_id}"
            )
            if new_sp != ch["setpoint"]:
                ch["setpoint"] = new_sp
                config["chillers"][ch_id - 1] = ch
                save_chiller_config(config)


# ---------------------------------------------------------
# HVAC Dashboard
# ---------------------------------------------------------
if view == "HVAC Dashboard":
    hvac_dashboard()


# ---------------------------------------------------------
# Single Chiller View
# ---------------------------------------------------------
if view == "Single Chiller":
    st.header(f"CH-{selected_chiller:02d}")
    ch = config["chillers"][selected_chiller - 1]
    sim = simulate_chiller_readings(ch["setpoint"])

    st.metric("Supply Temp", sim["supply_temp"])
    st.metric("Inlet Temp", sim["inlet_temp"])
    st.metric("Outlet Temp", sim["outlet_temp"])
    st.metric("Power", sim["power_kw"])


# ---------------------------------------------------------
# FULL VOICE-TO-VOICE STREAMING
# ---------------------------------------------------------
if view == "Voice-To-Voice":
    st.header("🎤 Voice Agent – Full Microphone Streaming")

    audio = st.audio_input("Speak to BMS Agent →")
    if audio:
        st.info("Processing...")
        text = transcribe_audio(audio.read())
        st.write(f"📢 You said: **{text}**")

        reply, updated = run_agent(text, config)
        config = updated
        save_chiller_config(config)

        st.success(reply)

        # TTS AUDIO OUTPUT
        speech = tts_speak(reply)
        st.audio(speech, format="audio/wav")
