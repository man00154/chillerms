import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _img(filename: str):
    full_path = os.path.join(BASE_DIR, filename)
    if os.path.isfile(full_path):
        st.image(full_path, use_column_width=True)
    else:
        st.error(f"⚠️ Image not found: {full_path}")

def show_layout(selection: str):
    if selection == "Cooling Layout":
        _img("cool1.png")
        _img("cool2.png")

    elif selection == "Single Chiller":
        _img("cool3.png")

    elif selection == "L1 Layout":
        _img("l1 chiller layout.png")
