import streamlit as st
import os
import base64

def inline_background_image(image_path: str) -> str:
    """
    Convert a local image file to a Base64 data URL for use in HTML background.
    """
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        return (
            f"background: url(data:image/png;base64,{encoded}) "
            f"center center / cover no-repeat;"
        )
    except FileNotFoundError:
        st.warning(f"Could not find the image at {image_path}")
        return ""

def render_header():
    """
    Renders a hero section with a Base64-encoded background image.
    """
    # Absolute path to 'header-bg.jpg' relative to this file
    image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "header-bg.jpg")

    # Convert the local image to a Base64 data URL
    bg_style = inline_background_image(image_path)

    # If no background is found, bg_style will be empty
    st.markdown(
        f"""
        <div class="hero-container" style="{bg_style}; 
             width:100%; 
             min-height:280px; 
             padding:2rem; 
             display:flex; 
             flex-direction:column; 
             justify-content:center;
             border-bottom:1px solid rgba(255,255,255,0.2);">
            <h1 class="hero-title">AI Travel Planner</h1>
            <p class="hero-subtitle">Your Personalized Adventure Assistant</p>
        </div>
        """,
        unsafe_allow_html=True
    )
