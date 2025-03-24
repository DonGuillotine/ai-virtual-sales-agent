"""Controller for managing application state."""
import os
import streamlit as st

def check_restart_typing():
    """Check if we need to reset the typing indicator."""
    if st.session_state.get("_reset_typing", False):
        st.session_state.is_typing = False
        st.session_state._reset_typing = False

def handle_message_queue():
    """Process any queued messages."""
    from controllers.chat_controller import process_message
    
    if st.session_state.get("process_message"):
        # Clear the message queue
        message = st.session_state.process_message
        st.session_state.process_message = None
        
        # Process the message
        success = process_message()
        
        # Set flag to reset typing indicator on next rerun
        st.session_state._reset_typing = True
        
        # Rerun to update UI
        st.rerun()

def update_display_state():
    """Update display state based on current application state."""
    # Handle pending approval
    if st.session_state.pending_approval:
        from ui.approval import handle_tool_approval
        handle_tool_approval(*st.session_state.pending_approval)