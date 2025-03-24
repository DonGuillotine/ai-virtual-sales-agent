"""
Main entry point for the Tech Shop Assistant application.
"""
import streamlit as st
from langchain_core.messages import HumanMessage

# Import UI components
from ui.config import set_page_config, set_page_style
from ui.sidebar import render_sidebar
from ui.chat import display_chat_history, handle_file_download

# Import controllers
from controllers.chat_controller import handle_user_input
from controllers.state_controller import check_restart_typing, handle_message_queue, update_display_state

# Import utilities
from utils.session_manager import initialize_session_state

def main():
    """Main application entry point."""
    # Initialize the application
    set_page_config()
    set_page_style()
    initialize_session_state()
    
    # Check for reset typing flag
    check_restart_typing()
    
    # Handle file downloads
    handle_file_download()
    
    # Render the sidebar
    render_sidebar()
    
    # Display chat history and UI components
    display_chat_history()
    
    # Update display state (e.g., handle pending approval)
    update_display_state()
    
    # Handle user input
    if prompt := st.chat_input("Ask me about our tech products..."):
        if handle_user_input(prompt):
            with st.chat_message("user"):
                st.write(prompt)
            
            # Queue message for processing after UI update
            st.session_state.process_message = prompt
            st.rerun()
    
    # Process any queued messages
    handle_message_queue()

if __name__ == "__main__":
    main()