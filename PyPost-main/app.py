"""
Gmail AI Assistant - Main Application
Minimalist email management with AI assistance
"""

import streamlit as st
from gmail_manager import GmailManager
from email_ai import EmailAI
from rag_chatbot import EmailRAGChatbot
from settings_ui import show_ai_settings, get_ai_settings
from ai_provider import get_ai_provider
from config import AI_CONFIG, AI_PROVIDERS, DEFAULT_AI_PROVIDER, TAB_NAMES

# Import UI components
def import_ui_components():
    from ui_components import (
        render_email_list_tab,
        render_smart_search_tab,
        render_summaries_tab,
        render_smart_reply_tab,
        render_analytics_tab,
        render_sentiment_tab,
        render_chatbot_tab
    )
    return (
        render_email_list_tab,
        render_smart_search_tab,
        render_summaries_tab,
        render_smart_reply_tab,
        render_analytics_tab,
        render_sentiment_tab,
        render_chatbot_tab
    )

# Import UI components
(
    render_email_list_tab,
    render_smart_search_tab,
    render_summaries_tab,
    render_smart_reply_tab,
    render_analytics_tab,
    render_sentiment_tab,
    render_chatbot_tab
) = import_ui_components()

# Removed compose modal for simplicity

def render_sidebar():
    """Render the sidebar with navigation and settings"""
    with st.sidebar:
        # Navigation
        st.markdown("### Navigation")
        
        # Navigation items
        nav_items = [
            ("📥 Inbox", "Inbox"),
            ("🔍 Smart Search", "Smart Search"),
            ("📋 Summaries", "Summaries"),
            ("💬 Smart Reply", "Smart Reply"),
            ("📊 Analytics", "Analytics"),
            ("🤖 Chatbot", "Chatbot")
        ]
        
        for icon, name in nav_items:
            if st.button(f"{icon} {name}", 
                       key=f"nav_{name.lower().replace(' ', '_')}", 
                       use_container_width=True,
                       type="primary" if st.session_state.get('active_tab') == name else "secondary"):
                st.session_state.active_tab = name
        
        st.markdown("---")
        
        # AI Settings Section
        with st.expander("⚙️ AI Settings", expanded=st.session_state.get('show_settings', False)):
            show_ai_settings()

def main():
    """Main application function"""
    # Initialize session state
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Inbox"
        st.session_state.gmail_authenticated = False
        st.session_state.gmail_auth_error = None
        st.session_state.gmail_auth_message = None
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    with st.container():
        # Get selected AI provider and settings
        ai_settings = get_ai_settings()
        
        # Initialize AI provider
        ai_provider = get_ai_provider(ai_settings["provider"])
        if not ai_provider:
            st.error("Please select an AI provider in settings")
            return
        
        # Initialize Gmail manager
        gmail_manager = GmailManager()
        
        # Handle Gmail authentication
        if not st.session_state.gmail_authenticated:
            if st.button("🔒 Connect Gmail"):
                with st.spinner("Authenticating with Gmail..."):
                    success = gmail_manager.authenticate()
                    if success:
                        st.session_state.gmail_authenticated = True
                        st.session_state.gmail_auth_message = "Successfully connected to Gmail"
                    else:
                        st.session_state.gmail_auth_error = "Failed to connect to Gmail. Please try again."
                        st.session_state.gmail_authenticated = False
            
            if st.session_state.gmail_auth_error:
                st.error(st.session_state.gmail_auth_error)
            elif st.session_state.gmail_auth_message:
                st.success(st.session_state.gmail_auth_message)
            
            return  # Don't proceed until authenticated
        
        # Initialize managers with AI provider
        email_ai = EmailAI(ai_provider)
        rag_chatbot = EmailRAGChatbot(ai_provider)
        
        # Check authentication state
        if not st.session_state.gmail_authenticated:
            if st.button("Connect Gmail", type="primary"):
                try:
                    if gmail_manager.authenticate():
                        st.session_state.gmail_authenticated = True
                        st.success("Successfully connected to Gmail")
                        st.rerun()
                    else:
                        st.error("Failed to authenticate with Gmail")
                except Exception as e:
                    st.error(f"Error during Gmail authentication: {str(e)}")
            return
        
        # Main interface with tabs
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(TAB_NAMES)
        
        with tab1:
            render_email_list_tab(gmail_manager, email_ai)
        
        with tab2:
            render_smart_search_tab(gmail_manager, email_ai)
        
        with tab3:
            render_summaries_tab(email_ai)
        
        with tab4:
            render_smart_reply_tab(gmail_manager, email_ai)
            
        with tab5:
            render_analytics_tab(gmail_manager, email_ai)
            
        with tab6:
            render_sentiment_tab(email_ai)
            
        with tab7:
            render_chatbot_tab(gmail_manager, rag_chatbot)


if __name__ == "__main__":
    main()