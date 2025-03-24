"""Chat UI components for the Tech Shop Assistant."""
import streamlit as st
from langchain_core.messages import HumanMessage

def display_chat_history():
    """Display the chat history and suggestions if empty."""
    if not st.session_state.messages:
        display_chat_suggestions()
    else:
        _render_messages()
    
    _display_typing_indicator()
    _display_error_message()

def _render_messages():
    """Render all messages in the chat history."""
    for message in st.session_state.messages:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.write(message.content)

def _display_typing_indicator():
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

def _display_error_message():
    """Display error message if any."""
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

def display_chat_suggestions():
    """Display interactive suggestion bubbles for the user organized by category."""
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

def handle_file_download():
    """Check for and handle file downloads."""
    import os
    
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