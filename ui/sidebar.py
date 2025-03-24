"""Sidebar components for the Tech Shop Assistant."""
import streamlit as st

def render_sidebar():
    """Render the sidebar with agent information and controls."""
    with st.sidebar:
        _render_agent_banner()
        _render_features_section()
        _render_categories_section()
        _render_action_buttons()
        _render_help_section()
        _render_custom_styles()

def _render_agent_banner():
    """Render the agent banner section."""
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

def _render_features_section():
    """Render the features section."""
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

def _render_categories_section():
    """Render the categories section."""
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

def _render_action_buttons():
    """Render action buttons."""
    st.markdown("""<div class="action-button-container">""", unsafe_allow_html=True)
    if st.button("🔄 New Conversation", key="new_chat_button", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.markdown("""</div>""", unsafe_allow_html=True)

def _render_help_section():
    """Render the help section."""
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

def _render_custom_styles():
    """Render custom CSS styles for the sidebar."""
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