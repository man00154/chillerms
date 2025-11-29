import os
import streamlit as st

BASE = os.path.dirname(os.path.abspath(__file__))

def _img(file):
    st.image(os.path.join(BASE, file), use_column_width=True)

def show_layout(view):
    if view == "L1 Layout":
        _img("l1 chiller layout.png")

    elif view == "Cooling Layout":
        _img("cool1.png")
        _img("cool2.png")

    elif view == "Single Chiller":
        _img("cool3.png")
