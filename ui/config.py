"""UI configuration module for the Tech Shop Assistant."""
import streamlit as st

def set_page_config():
    """Set the Streamlit page configuration."""
    st.set_page_config(
        page_title="Tech Shop Assistant",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def set_page_style():
    """Set the page custom CSS styling."""
    try:
        with open("assets/style.css", "r") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load CSS: {str(e)}")git a