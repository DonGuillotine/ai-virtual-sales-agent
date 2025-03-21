import json
import os
import uuid
import time

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages.tool import ToolMessage

from virtual_sales_agent.graph import graph


def set_page_config():
    st.set_page_config(
        page_title="Tech Shop Assistant",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def set_page_style():
    st.markdown(
        f"""
        <style>
        {open("assets/style.css").read()}
        </style>
    """,
        unsafe_allow_html=True,
    )


def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    if "pending_approval" not in st.session_state:
        st.session_state.pending_approval = None

    if "config" not in st.session_state:
        st.session_state.config = {
            "configurable": {
                "customer_id": "123456789",
                "thread_id": st.session_state.thread_id,
            }
        }

    if "is_typing" not in st.session_state:
        st.session_state.is_typing = False

    if "error" not in st.session_state:
        st.session_state.error = None


def setup_sidebar():
    """Configure the sidebar with agent information and controls."""
    with st.sidebar:
        # Agent banner section
        st.markdown(
            """
            <div class="agent-profile">
                <div class="agent-banner">
                    <div class="agent-banner-content">
                        <div class="avatar">🤖</div>
                        <h1>AI Tech Advisor</h1>
                    </div>
                </div>
                <div class="agent-status">
                    <div class="status-indicator"></div>
                    <span>Online & Ready</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Features section
        st.markdown(
            """
            <div class="sidebar-section">
                <h3>What I Can Do</h3>
                <div class="feature-grid">
                    <div class="feature-item">
                        <div class="feature-icon">🔍</div>
                        <div class="feature-text">Find Products</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">👨‍💻</div>
                        <div class="feature-text">Tech Advice</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🛒</div>
                        <div class="feature-text">Place Orders</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🚚</div>
                        <div class="feature-text">Track Orders</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Categories section
        st.markdown(
            """
            <div class="sidebar-section">
                <h3>Recent Categories</h3>
                <div class="category-tags">
                    <div class="category-tag">Gaming Mice</div>
                    <div class="category-tag">Laptops</div>
                    <div class="category-tag">Keyboards</div>
                    <div class="category-tag">Smartphones</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Custom new chat button with special styling
        st.markdown("""<div class="action-button-container">""", unsafe_allow_html=True)
        if st.button("🔄 New Conversation", key="new_chat_button", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown("""</div>""", unsafe_allow_html=True)
        
        # Help section
        st.markdown(
            """
            <div class="help-section">
                <h3>Need Help?</h3>
                <p>Our customer service team is available 24/7 to assist you with any questions or concerns.</p>
                <div class="help-contact">
                    <div class="help-contact-item">
                        <span class="contact-icon">📞</span>
                        <span>+234 81 6236 3061</span>
                    </div>
                    <div class="help-contact-item">
                        <span class="contact-icon">✉️</span>
                        <span>infect3dlab@gmail.com</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Custom CSS for the new chat button
        st.markdown(
            """
            <style>
            /* Style for the new chat button */
            .action-button-container button {
                background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
                border: none;
                padding: 1rem 1.5rem;
                border-radius: 1rem;
                color: white;
                font-weight: 600;
                box-shadow: 0 4px 15px rgba(108, 62, 244, 0.3);
                transition: all 0.3s ease;
                margin: 1rem 0 1.5rem 0;
            }
            
            .action-button-container button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(108, 62, 244, 0.4);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


def display_chat_suggestions():
    """Display interactive suggestion bubbles for the user organized by category."""
    if not st.session_state.messages:
        primary_suggestions = [
            "I want to order the Alienware m17 R5",
            "Check the status of my order",
            "What is your return policy?",
            "I'd like to speak with a human representative",
            "Show me your best-selling products"
        ]
        
        product_suggestions = [
            "Which Logitech mouse is best for big hands?",
            "Compare Samsung Galaxy S21 vs S22",
            "What's your best gaming laptop under $1500?",
            "Recommend a webcam for streaming",
            "What mechanical keyboard should I buy?"
        ]
        
        st.markdown(
            """
            <div style='text-align: center; padding: 30px;'>
                <h1>👋 Welcome to Tech Shop!</h1>
                <p>How can I assist you with your tech needs today?</p>
            </div>
            <div style='margin-bottom: 16px;'>
                <h3 style='color: #9b51e0; margin-bottom: 12px; font-size: 18px; text-align: center;'>I can help you with:</h3>
                <div class="suggestions-container">
            """
            + "".join([f'<div class="suggestion-bubble primary-suggestion" onclick="parent.postMessage({{suggestion: \'{s}\'}}, \'*\')">{s}</div>' for s in primary_suggestions])
            + """
                </div>
            </div>
            <div>
                <h3 style='color: #9b51e0; margin-bottom: 12px; font-size: 18px; text-align: center;'>Looking for product recommendations?</h3>
                <div class="suggestions-container">
            """
            + "".join([f'<div class="suggestion-bubble product-suggestion" onclick="parent.postMessage({{suggestion: \'{s}\'}}, \'*\')">{s}</div>' for s in product_suggestions])
            + """
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # JavaScript to handle the suggestion clicks
        st.markdown(
            """
            <script>
            window.addEventListener('message', function(e) {
                if (e.data.suggestion) {
                    const input = window.parent.document.querySelector('.stChatInputContainer textarea');
                    if (input) {
                        input.value = e.data.suggestion;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        const submitButton = window.parent.document.querySelector('.stChatInputContainer button');
                        if (submitButton) {
                            submitButton.click();
                        }
                    }
                }
            });
            </script>
            """,
            unsafe_allow_html=True,
        )
        
              
def display_typing_indicator():
    """Display typing indicator when the assistant is generating a response."""
    if st.session_state.is_typing:
        st.markdown(
            """
            <div class="typing-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def display_chat_history():
    """Display the chat history."""
    display_chat_suggestions()
    
    for message in st.session_state.messages:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.write(message.content)
    
    display_typing_indicator()
    
    if st.session_state.error:
        st.markdown(
            f"""
            <div class="error-message">
                <div class="error-icon">⚠️</div>
                <div>{st.session_state.error}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def process_events(event):
    """Process events from the graph and extract messages."""
    seen_ids = set()

    if isinstance(event, dict) and "messages" in event:
        messages = event["messages"]
        last_message = messages[-1] if messages else None

        if isinstance(last_message, AIMessage):
            if last_message.id not in seen_ids and last_message.content:
                seen_ids.add(last_message.id)
                st.session_state.messages.append(last_message)
                with st.chat_message("assistant"):
                    st.write(last_message.content)

            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return last_message.tool_calls[0]

    return None


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
                    result = graph.invoke(None, st.session_state.config)
                    process_events(result)
                    st.session_state.pending_approval = None
                    st.rerun()
                except Exception as e:
                    st.session_state.error = f"Error processing approval: {str(e)}"
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="deny-btn">', unsafe_allow_html=True)
        if st.button("❌ Deny Action", use_container_width=True):
            st.session_state.show_reason_input = True
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("show_reason_input", False):
        reason = st.text_input("Please explain why you're denying this action:")
        submit = st.button("Submit Denial", key="submit_denial")
        if reason and submit:
            with st.spinner("Processing your denial..."):
                try:
                    result = graph.invoke(
                        {
                            "messages": [
                                ToolMessage(
                                    tool_call_id=last_message.tool_calls[0]["id"],
                                    content=f"API call denied by user. Reasoning: '{reason}'. Continue assisting, accounting for the user's input.",
                                )
                            ]
                        },
                        st.session_state.config,
                    )
                    process_events(result)
                    st.session_state.pending_approval = None
                    st.session_state.show_reason_input = False
                    st.rerun()
                except Exception as e:
                    st.session_state.error = f"Error processing denial: {str(e)}"

    st.markdown('</div>', unsafe_allow_html=True)


def main():
    set_page_config()
    set_page_style()
    initialize_session_state()
    setup_sidebar()
    
    if st.session_state.get("_reset_typing", False):
        st.session_state.is_typing = False
        st.session_state._reset_typing = False
        
    # Check for download marker before anything else
    if os.path.exists("download_ready.txt"):
        try:
            with open("download_ready.txt", "r") as f:
                download_path = f.read().strip()
            
            if os.path.exists(download_path):
                with open(download_path, "r") as file:
                    csv_content = file.read()
                
                # Remove the marker file
                os.remove("download_ready.txt")
                
                # Place the download button prominently in the UI
                st.success("✅ Your request has been successfully recorded!")
                st.download_button(
                    label="📥 Download Your Support Request",
                    data=csv_content,
                    file_name="support_request.csv",
                    mime="text/csv",
                )
        except Exception as e:
            st.error(f"Error preparing download: {e}")

    display_chat_history()

    if st.session_state.pending_approval:
        handle_tool_approval(*st.session_state.pending_approval)

    if prompt := st.chat_input("Ask me about our tech products..."):
        st.session_state.error = None
        human_message = HumanMessage(content=prompt)
        st.session_state.messages.append(human_message)
        with st.chat_message("user"):
            st.write(prompt)

        # Set typing indicator and create a flag to process the message
        st.session_state.is_typing = True
        st.session_state.process_message = prompt
        st.rerun()

    # Process any message after the UI has been updated with typing indicator
    if st.session_state.get("process_message"):
        prompt = st.session_state.process_message
        st.session_state.process_message = None
        
        try:
            events = list(
                graph.stream(
                    {"messages": st.session_state.messages},
                    st.session_state.config,
                    stream_mode="values",
                )
            )
            
            last_event = events[-1] if events else None
            if last_event:
                tool_call = process_events(last_event)

                if tool_call:
                    snapshot = graph.get_state(st.session_state.config)
                    if snapshot.next:
                        st.session_state.pending_approval = (snapshot, events[-1])
            
            # Set flag to reset typing indicator on next rerun
            st.session_state._reset_typing = True
            st.rerun()
                
        except Exception as e:
            st.session_state.error = f"Error processing message: {str(e)}"
            st.session_state._reset_typing = True
            st.rerun()


if __name__ == "__main__":
    main()