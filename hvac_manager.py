import random
import streamlit as st

# ----------------------------------------------------
# Generate simulated HVAC values
# ----------------------------------------------------
def generate_hvac_values():
    return {
        "ahu_temp": round(random.uniform(19, 24), 2),
        "ahu_rh": round(random.uniform(40, 55), 2),
        "pahu_temp": round(random.uniform(19, 24), 2),
        "pahu_rh": round(random.uniform(38, 52), 2),
        "tfa_temp": round(random.uniform(18, 23), 2),
        "tfa_rh": round(random.uniform(35, 50), 2),
    }


# ----------------------------------------------------
# HVAC Dashboard UI (AHU + PAHU + TFA)
# ----------------------------------------------------
def hvac_dashboard():
    st.subheader("AHU + PAHU + TFA Dashboard (Simulated Values)")
    hvac = generate_hvac_values()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### AHU")
        st.metric("Supply Temp (°C)", hvac["ahu_temp"])
        st.metric("Humidity (%)", hvac["ahu_rh"])

    with col2:
        st.markdown("### PAHU")
        st.metric("Supply Temp (°C)", hvac["pahu_temp"])
        st.metric("Humidity (%)", hvac["pahu_rh"])

    with col3:
        st.markdown("### TFA")
        st.metric("Fresh Air Temp (°C)", hvac["tfa_temp"])
        st.metric("Humidity (%)", hvac["tfa_rh"])
