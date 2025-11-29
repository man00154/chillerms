import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _img(name):
    full = os.path.join(BASE_DIR, name)
    if os.path.isfile(full):
        st.image(full, use_column_width=True)
    else:
        st.error(f"Image missing: {full}")

def show_layout(view):
    if view == "Cooling":
        _img("cool1.png")
        _img("cool2.png")
    elif view == "Chiller":
        _img("cool3.png")
    elif view == "L1 Layout":
        _img("l1 chiller layout.png")
