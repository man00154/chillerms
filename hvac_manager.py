import streamlit as st
from api_client import get_hvac_data

def hvac_dashboard():
    data = get_hvac_data()

    st.subheader("AHU / PAHU / TFA Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("AHU Temp (°C)", data["ahu_temp"])
    col1.metric("AHU RH (%)", data["ahu_rh"])

    col2.metric("PAHU Temp (°C)", data["pahu_temp"])
    col2.metric("PAHU RH (%)", data["pahu_rh"])

    col3.metric("TFA Temp (°C)", data["tfa_temp"])
    col3.metric("TFA RH (%)", data["tfa_rh"])
