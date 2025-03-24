"""Tool approval UI components for the Tech Shop Assistant."""
import json
import streamlit as st
from langchain_core.messages import AIMessage, ToolMessage

from services.graph_service import invoke_graph, get_graph_state

def handle_tool_approval(snapshot, event):
    """Handle tool approval process with improved UI."""
    st.markdown(
        """
        <div class="tool-approval-card">
            <div class="tool-header">
                <div class="tool-icon">🔧</div>
                <div class="tool-title">Action Approval Required</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    last_message = snapshot.values.get("messages", [])[-1]

    if (
        isinstance(last_message, AIMessage)
        and hasattr(last_message, "tool_calls")
        and last_message.tool_calls
    ):
        tool_call = last_message.tool_calls[0]
        
        st.markdown("#### The assistant wants to perform the following action:")
        
        with st.expander("View Function Details", expanded=True):
            st.info(f"Function: **{tool_call['name']}**")

            try:
                args_formatted = json.dumps(tool_call['args'], indent=2)
                st.code(f"Arguments:\n{args_formatted}", language="json")
            except:
                st.code(f"Arguments:\n{tool_call['args']}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="approve-btn">', unsafe_allow_html=True)
        if st.button("✅ Approve Action", use_container_width=True):
            with st.spinner("Processing your approval..."):
                try:
                    result = invoke_graph(None)
                    _process_approval_result(result)
                except Exception as e:
                    st.session_state.error = f"Error processing approval: {str(e)}"
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="deny-btn">', unsafe_allow_html=True)
        if st.button("❌ Deny Action", use_container_width=True):
            st.session_state.show_reason_input = True
        st.markdown('</div>', unsafe_allow_html=True)

    _handle_denial_input(last_message)

    st.markdown('</div>', unsafe_allow_html=True)

def _handle_denial_input(last_message):
    """Handle the denial input form."""
    if st.session_state.get("show_reason_input", False):
        reason = st.text_input("Please explain why you're denying this action:")
        submit = st.button("Submit Denial", key="submit_denial")
        if reason and submit:
            with st.spinner("Processing your denial..."):
                try:
                    messages_payload = {
                        "messages": [
                            ToolMessage(
                                tool_call_id=last_message.tool_calls[0]["id"],
                                content=f"API call denied by user. Reasoning: '{reason}'. Continue assisting, accounting for the user's input.",
                            )
                        ]
                    }
                    result = invoke_graph(messages_payload)
                    _process_approval_result(result)
                except Exception as e:
                    st.session_state.error = f"Error processing denial: {str(e)}"

def _process_approval_result(result):
    """Process the result of approval or denial."""
    from controllers.chat_controller import process_events
    
    process_events(result)
    st.session_state.pending_approval = None
    st.session_state.show_reason_input = False
    st.rerun()