import os
import streamlit as st
from PIL import Image

# Base directory = folder where layout_manager.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _img(filename: str):
    """
    Safely load images that are in the same folder
    as app.py and layout_manager.py (no assets/ subfolder).
    """
    full_path = os.path.join(BASE_DIR, filename)

    if os.path.isfile(full_path):
        st.image(full_path, use_column_width=True)
    else:
        st.error(f"⚠️ Image not found: {full_path}")

def show_layout(selection: str):
    """
    Switches layout based on sidebar selection.
    """
    if selection == "Cooling":
        _img("cool1.png")
        _img("cool2.png")

    elif selection == "Chiller":
        _img("cool3.png")

    elif selection == "L1 Layout":
        # Use the exact filename with spaces as in your repo
        _img("l1 chiller layout.png")
