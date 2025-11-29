import streamlit as st
from PIL import Image

def show_layout(selection):
    if selection == "Cooling":
        st.image("assets/cool1.png")
    elif selection == "Chiller":
        st.image("assets/cool3.png")
    elif selection == "L1 Layout":
        st.image("assets/l1_chiller_layout.png")
