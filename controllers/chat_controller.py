"""Controller for chat interactions."""
import streamlit as st
from langchain_core.messages import HumanMessage

from services.graph_service import stream_graph, extract_tool_call, get_graph_state, process_result

# Keep track of seen message IDs to avoid duplicates
_SEEN_MESSAGE_IDS = set()

def handle_user_input(prompt):
    """
    Handle user input and generate a response.
    
    Args:
        prompt: The user's message.
        
    Returns:
        True if processing was successful, False otherwise.
    """
    from utils.session_manager import clear_error, set_typing_state

    # Reset error state
    clear_error()
    
    # Add user message to chat history
    human_message = HumanMessage(content=prompt)
    st.session_state.messages.append(human_message)
    
    # Set typing indicator
    set_typing_state(True)
    
    return True

def process_message():
    """
    Process the pending message and update the UI.
    
    Returns:
        True if processing was successful, False otherwise.
    """
    from utils.session_manager import set_typing_state, set_error
    
    global _SEEN_MESSAGE_IDS
    
    try:
        # Get current message history
        events = stream_graph(st.session_state.messages)
        
        # Extract the last event
        last_event = events[-1] if events else None
        if last_event:
            # Process the event to extract messages
            _SEEN_MESSAGE_IDS, last_message = process_result(last_event, _SEEN_MESSAGE_IDS)
            
            # Add message to chat history if new
            if last_message:
                st.session_state.messages.append(last_message)
            
            # Check for tool calls
            tool_call = extract_tool_call(last_event)
            if tool_call:
                snapshot = get_graph_state()
                if snapshot.next:
                    st.session_state.pending_approval = (snapshot, events[-1])
        
        # Reset typing indicator
        set_typing_state(False)
        return True
        
    except Exception as e:
        set_error(f"Error processing message: {str(e)}")
        set_typing_state(False)
        return False

def process_events(event):
    """
    Process events from the graph and extract messages.
    For use with tool approval flows.
    
    Args:
        event: The event to process.
        
    Returns:
        The extracted tool call, if any.
    """
    global _SEEN_MESSAGE_IDS
    
    _SEEN_MESSAGE_IDS, last_message = process_result(event, _SEEN_MESSAGE_IDS)
    
    if last_message:
        st.session_state.messages.append(last_message)
        with st.chat_message("assistant"):
            st.write(last_message.content)
    
    return extract_tool_call(event)