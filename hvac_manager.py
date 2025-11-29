import random
import streamlit as st

def hvac_dashboard():
    st.header("AHU + PAHU + TFA Dashboard (Simulated)")

    data = {
        "ahu_temp": round(random.uniform(19, 24), 2),
        "ahu_rh": round(random.uniform(40, 55), 2),
        "pahu_temp": round(random.uniform(19, 23), 2),
        "pahu_rh": round(random.uniform(38, 52), 2),
        "tfa_temp": round(random.uniform(18, 22), 2),
        "tfa_rh": round(random.uniform(35, 50), 2)
    }

    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("AHU")
        st.metric("Temp (°C)", data["ahu_temp"])
        st.metric("Humidity (%)", data["ahu_rh"])

    with c2:
        st.subheader("PAHU")
        st.metric("Temp (°C)", data["pahu_temp"])
        st.metric("Humidity (%)", data["pahu_rh"])

    with c3:
        st.subheader("TFA")
        st.metric("Fresh Air (°C)", data["tfa_temp"])
        st.metric("Humidity (%)", data["tfa_rh"])
