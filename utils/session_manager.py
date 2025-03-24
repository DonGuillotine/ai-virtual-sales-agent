"""Session state management utilities."""
import uuid
import streamlit as st

def initialize_session_state():
    """Initialize all session state variables."""
    # Chat state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Thread/customer identification
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    # Tool approval state
    if "pending_approval" not in st.session_state:
        st.session_state.pending_approval = None

    # Configuration
    if "config" not in st.session_state:
        st.session_state.config = {
            "configurable": {
                "customer_id": "123456789",
                "thread_id": st.session_state.thread_id,
            }
        }

    # UI state
    if "is_typing" not in st.session_state:
        st.session_state.is_typing = False

    # Error handling
    if "error" not in st.session_state:
        st.session_state.error = None

def reset_session_state():
    """Reset all session state variables."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def get_config():
    """Get the current configuration."""
    return st.session_state.config

def set_typing_state(is_typing):
    """Set the typing indicator state."""
    st.session_state.is_typing = is_typing

def set_error(error_message):
    """Set an error message."""
    st.session_state.error = error_message

def clear_error():
    """Clear the error message."""
    st.session_state.error = None