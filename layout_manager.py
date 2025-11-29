import os
import streamlit as st

# Base directory (same folder as app.py and PNGs)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _img(file):
    """Display PNG from same directory."""
    full = os.path.join(BASE_DIR, file)
    if os.path.isfile(full):
        st.image(full, use_column_width=True)
    else:
        st.error(f"Image not found: {full}")


def show_layout(view: str):
    """
    Display layout images as per user selection.
    """
    if view == "L1 Layout":
        _img("l1 chiller layout.png")

    elif view == "Cooling Layout":
        _img("cool1.png")
        _img("cool2.png")

    elif view == "Single Chiller Layout":
        _img("cool3.png")
