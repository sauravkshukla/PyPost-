"""
Simplified UI Components for the Gmail AI Assistant
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from config import SEARCH_EXAMPLES, REPLY_TONES

# Utility to clear only relevant session state keys
def clear_tab_state(prefix: str) -> None:
    """Clear session state keys with the given prefix"""
    keys_to_clear = [k for k in st.session_state.keys() if k.startswith(prefix)]
    for k in keys_to_clear:
        del st.session_state[k]

def get_icon_for_sender(sender: str) -> str:
    """Get an appropriate icon for the email sender"""
    sender_lower = sender.lower()
    if any(domain in sender_lower for domain in ['support', 'help', 'service']):
        return '🛟'
    elif any(domain in sender_lower for domain in ['notification', 'alert', 'update']):
        return '🔔'
    elif any(domain in sender_lower for domain in ['news', 'update', 'blog']):
        return '📰'
    elif any(domain in sender_lower for domain in ['team', 'hr', 'people']):
        return '👥'
    return '✉️'

def format_date(date_str: str) -> str:
    """Format date string to a more readable format"""
    try:
        date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        now = datetime.now(date_obj.tzinfo)
        
        if date_obj.date() == now.date():
            return date_obj.strftime('%I:%M %p')
        elif (now.date() - date_obj.date()).days == 1:
            return 'Yesterday'
        elif (now.date() - date_obj.date()).days < 7:
            return date_obj.strftime('%A')
        else:
            return date_obj.strftime('%b %d')
    except:
        return date_str

def render_sidebar_config():
    """Render sidebar configuration with modern styling"""
    with st.sidebar.expander("⚙️ Display Settings", expanded=False):
        st.selectbox(
            "Email View",
            ["Compact", "Comfortable", "Detailed"],
            key="sidebar_email_view_mode",  # Unique key with prefix
            help="Change how emails are displayed"
        )
        
        st.slider(
            "Emails per page",
            min_value=5,
            max_value=50,
            value=20,
            step=5,
            key="sidebar_emails_per_page",  # Unique key with prefix
            help="Number of emails to show per page"
        )
        
        st.toggle(
            "Show unread only",
            value=False,
            key="sidebar_show_unread_only",  # Unique key with prefix
            help="Only show unread emails"
        )
    
    gemini_api_key = st.sidebar.text_input(
        "Google Gemini API Key", 
        type="password",
        help="Enter your Google Gemini API key"
    )
    
    return gemini_api_key


def render_setup_instructions():
    """Render setup instructions when API key is not provided"""
    st.title("Welcome to Gmail AI Assistant")
    
    # Introduction
    st.markdown("""
    ## Get Started with AI-Powered Email Management
    
    This application helps you manage your Gmail inbox using advanced AI capabilities from multiple providers.
    Choose the AI provider that best suits your needs and budget.
    """)
    
    # AI Provider Information
    st.markdown("## Supported AI Providers")
    
    # Create columns for each provider
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("🤖 Google Gemini", expanded=True):
            st.markdown("""
            **Free Models Available:**
            - Gemini 2.5 Flash (Recommended)
            - Gemini 1.5 Pro
            
            **Paid Models:**
            - Gemini 2.0 Pro
            - Gemini 1.0 Ultra
            
            [Get API Key](https://makersuite.google.com/app/apikey)
            """)
    
    with col2:
        with st.expander("🔮 OpenAI", expanded=True):
            st.markdown("""
            **Free Tier Available** (with limitations)
            
            **Models:**
            - GPT-4o (Recommended)
            - GPT-4
            - GPT-3.5 Turbo
            
            [Get API Key](https://platform.openai.com/api-keys)
            """)
    
    col3, col4 = st.columns(2)
    
    with col3:
        with st.expander("🤖 Anthropic Claude", expanded=True):
            st.markdown("""
            **Free Trial Available**
            
            **Models:**
            - Claude 3 Opus
            - Claude 3 Sonnet
            - Claude 3 Haiku
            
            [Get API Key](https://console.anthropic.com/settings/keys)
            """)
    
    with col4:
        with st.expander("🚀 xAI Grok", expanded=True):
            st.markdown("""
            **Currently in Beta**
            
            **Models:**
            - Grok-1.5
            - Grok-1.5 Vision
            
            [Learn More](https://x.ai/)
            """)
    
    # Setup Instructions
    st.markdown("""
    ## Setup Instructions
    
    1. **Choose an AI Provider** and get your API key from their website
    2. Enter your API key in the sidebar
    3. Download your Gmail API `credentials.json` from [Google Cloud Console](https://console.cloud.google.com/)
    4. Place `credentials.json` in the same directory as this app
    5. Install required packages:
       ```bash
       pip install -r requirements.txt
       ```
    6. Run the app: `streamlit run app.py`
    7. Authenticate with Gmail when prompted
    """)


def render_authentication_section(gmail_manager):
    """Render Gmail authentication section"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        # Network diagnostics section
        with st.expander("🔧 Network Diagnostics", expanded=False):
            from utils import test_network_connectivity, check_gmail_api_access, get_network_info, handle_ssl_error
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🌐 Test Internet Connection"):
                    if test_network_connectivity():
                        st.success("✅ Internet connection is working")
                    else:
                        st.error("❌ Internet connection failed")
            
            with col2:
                if st.button("📧 Test Gmail API Access"):
                    if check_gmail_api_access():
                        st.success("✅ Gmail API is accessible")
                    else:
                        st.error("❌ Gmail API access failed")
            
            # Show network info
            network_info = get_network_info()
            st.write("**Network Information:**")
            for key, value in network_info.items():
                st.write(f"- {key}: {value}")
        
        if st.button("🔐 Authenticate with Gmail"):
            with st.spinner("Authenticating with Gmail..."):
                try:
                    if gmail_manager.authenticate():
                        st.session_state.authenticated = True
                        st.session_state.gmail_manager = gmail_manager
                        st.success("Successfully authenticated with Gmail!")
                        st.rerun()
                    else:
                        st.error("Authentication failed. Please check your credentials.json file.")
                except Exception as e:
                    error_info = handle_ssl_error(e)
                    st.error(f"Authentication error: {error_info['message']}")
                    st.write("**Possible solutions:**")
                    for solution in error_info['solutions']:
                        st.write(f"- {solution}")
        return False
    
    return True


def render_email_list_tab(gmail_manager, email_ai):
    """Render the email list tab with simplified UI"""
    st.title("Email List")
    
    # Add search bar
    search_query = st.text_input("Search emails", "")
    
    # Add view mode selector
    view_mode = st.selectbox("View Mode", ["All", "Unread", "Starred", "Important"])
    
    # Add authentication check
    if not gmail_manager.service:
        st.error("Please authenticate with Gmail first")
        return
    
    # Add max emails slider
    max_emails = st.slider("Number of emails to display", 1, 100, 50)
    
    # Fetch emails based on view mode
    emails = []
    query = ""
    
    if view_mode == "All":
        query = ""
    elif view_mode == "Unread":
        query = "is:unread"
    elif view_mode == "Starred":
        query = "is:starred"
    elif view_mode == "Important":
        query = "is:important"
    
    messages = gmail_manager.get_messages(query=query, max_results=max_emails)
    
    # Process messages to get email details
    for msg in messages:
        email_details = gmail_manager.get_message_details(msg['id'])
        if email_details:
            content = gmail_manager.extract_email_content(email_details)
            emails.append(content)
    
    # Display emails in a simple list
    for email in emails:
        with st.expander(f"📧 {email['subject']}"):
            st.write(f"From: {email['sender']}")
            st.write(f"Date: {email['date']}")
            st.write(f"Content: {email['body'][:500]}...")
            
            # Email actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Reply"):
                    st.session_state[f"email_to_reply_{email['id']}"] = email
                    st.rerun()
            with col2:
                if st.button("Summarize"):
                    st.session_state[f"email_to_summarize_{email['id']}"] = email
                    st.rerun()
            with col3:
                if st.button("Analyze"):
                    st.session_state[f"email_to_analyze_{email['id']}"] = email
                    st.rerun()
                st.write(email.get('body', 'No content'))
                
                # Add action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Reply to this email", key=f"reply_{i}"):
                        st.session_state.replying_to = email
                with col2:
                    if st.button(f"Forward this email", key=f"forward_{i}"):
                        st.session_state.forwarding = email
                
                # Add additional actions
                with st.expander("More actions"):
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"⭐ Star email", key=f"star_{i}"):
                            st.session_state.email_action = f"star_{i}"
                        if st.button(f"📝 Summarize email", key=f"summarize_{i}"):
                            st.session_state.email_action = f"summarize_{i}"
                    with col2:
                        if st.button(f"🗄️ Archive email", key=f"archive_{i}"):
                            st.session_state.email_action = f"archive_{i}"
                
                # Add some spacing between emails
                st.write("")
                st.write("---")
                
                # Handle email actions
                if f'email_action' in st.session_state:
                    action, idx = st.session_state.email_action.split('_')
                    if int(idx) == i:
                        if action == 'summarize':
                            clear_tab_state("email_to_summarize_")
                            st.session_state[f"email_to_summarize_{i}"] = email
                            st.session_state.active_tab = 'summaries'
                            del st.session_state['email_action']
                            st.rerun()
                        elif action == 'reply':
                            clear_tab_state("email_to_reply_")
                            st.session_state[f"email_to_reply_{i}"] = email
                            st.session_state.active_tab = 'smart_reply'
                            del st.session_state['email_action']
                            st.rerun()
    
    # Add custom CSS for email cards
    st.markdown("""
    <style>
        .email-card {
            transition: all 0.2s ease-in-out;
        }
        .email-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        .email-action-btn {
            background: none;
            border: none;
            font-size: 1.1rem;
            cursor: pointer;
            opacity: 0.6;
            transition: all 0.2s;
        }
        .email-action-btn:hover {
            opacity: 1;
            transform: scale(1.1);
        }
        .action-btn {
            background: #F1F5F9;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 0.35rem 0.75rem;
            font-size: 0.85rem;
            color: #475569;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        .action-btn:hover {
            background: #E2E8F0;
        }
    </style>
    <script>
    // Make sure Streamlit is defined
    if (window.Streamlit) {
        window.streamlitRun = function(code) {
            const script = document.createElement('script');
            script.type = 'text/plain';
            script.text = code;
            document.body.appendChild(script);
            window.parent.postMessage({
                type: 'streamlit:runScript',
                data: script.text
            }, '*');
            document.body.removeChild(script);
        }
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Add a nice empty state if no emails match the filter
    if not messages or (view_mode == "Unread" and not any(email.get('unread', False) for email in emails_data)):
        st.markdown("""
        <div style="
            text-align: center;
            padding: 3rem 1rem;
            background: #F8FAFC;
            border-radius: 12px;
            margin: 2rem 0;
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📭</div>
            <h3 style="color: #1E293B; margin-bottom: 0.5rem;">No emails found</h3>
            <p style="color: #64748B; margin: 0;">
                {}
            </p>
        </div>
        """.format(
            "No unread emails" if view_mode == "Unread" else 
            "No emails match your search" if search_query else 
            "Your inbox is empty"
        ), unsafe_allow_html=True)


def render_smart_search_tab(gmail_manager, email_ai):
    """Render the smart search tab"""
    st.header("Smart Email Search")
    
    search_query = st.selectbox(
        "Choose a search example or enter your own:",
        [""] + SEARCH_EXAMPLES
    )
    
    custom_query = st.text_input("Or enter custom search query:")
    
    if custom_query:
        search_query = custom_query
    
    if search_query:
        if st.button("🔍 Search"):
            # Convert natural language to Gmail search query
            if "jobs" in search_query.lower() or "career" in search_query.lower():
                gmail_query = "from:(linkedin.com OR indeed.com OR glassdoor.com) OR subject:(job OR career OR opportunity OR hiring)"
            elif "meeting" in search_query.lower():
                gmail_query = "subject:(meeting OR call OR zoom OR teams)"
            elif "urgent" in search_query.lower():
                gmail_query = "subject:(urgent OR important OR ASAP)"
            elif "newsletter" in search_query.lower():
                gmail_query = "subject:(newsletter OR update OR digest)"
            else:
                gmail_query = search_query
            
            with st.spinner("Searching emails..."):
                messages = gmail_manager.get_messages(query=gmail_query, max_results=20)
            
            if messages:
                st.success(f"Found {len(messages)} emails matching your search.")
                
                for msg in messages:
                    email_details = gmail_manager.get_message_details(msg['id'])
                    if email_details:
                        content = gmail_manager.extract_email_content(email_details)
                        with st.expander(f"📧 {content['subject']} - {content['sender']}"):
                            st.write(f"**From:** {content['sender']}")
                            st.write(f"**Date:** {content['date']}")
                            st.write(f"**Subject:** {content['subject']}")
                            st.text(content['body'][:300] + "..." if len(content['body']) > 300 else content['body'])
            else:
                st.info("No emails found matching your search criteria.")


def render_summaries_tab(email_ai):
    """Render the summaries tab"""
    st.header("Email Summaries")
    
    found = False
    for key in st.session_state.keys():
        if key.startswith("email_to_summarize_"):
            found = True
            email = st.session_state[key]
            st.subheader(f"Summary for: {email['subject']}")
            
            with st.spinner("Generating summary with Gemini..."):
                summary = email_ai.summarize_email(email)
            
            st.write("**AI Summary:**")
            st.write(summary)
            
            # Extract action items
            with st.spinner("Extracting action items..."):
                actions = email_ai.extract_action_items(email)
            
            st.write("**Action Items:**")
            st.write(actions)
            
            if st.button("Clear Summary Result"):
                clear_tab_state("email_to_summarize_")
                st.rerun()
            break
    if not found:
        st.info("Select an email from the Email List tab to summarize.")


def render_smart_reply_tab(gmail_manager, email_ai):
    """Render the smart reply tab"""
    st.header("Smart Reply Generator")
    
    found = False
    for key in st.session_state.keys():
        if key.startswith("email_to_reply_"):
            found = True
            email = st.session_state[key]
            st.subheader(f"Reply to: {email['subject']}")
            
            # Reply tone selection
            tone = st.selectbox("Select reply tone:", REPLY_TONES)
            
            if st.button("Generate Reply"):
                with st.spinner("Generating smart reply with Gemini..."):
                    reply = email_ai.generate_smart_reply(email, tone)
                
                st.write("**Generated Reply:**")
                st.text_area("Reply content:", reply, height=200)
                
                # Option to send reply
                if st.button("📤 Send Reply"):
                    sender_email = gmail_manager.extract_sender_email(email['sender'])
                    
                    result = gmail_manager.send_reply(
                        email['thread_id'],
                        sender_email,
                        email['subject'],
                        reply
                    )
                    
                    if result:
                        st.success("Reply sent successfully!")
                    else:
                        st.error("Failed to send reply.")
            
            if st.button("Clear Reply Result"):
                clear_tab_state("email_to_reply_")
                st.rerun()
            break
    
    if not found:
        st.info("Select an email from the Email List tab to generate a reply.")


def render_analytics_tab(gmail_manager, email_ai):
    """Render the analytics tab"""
    st.header("Email Analytics")
    
    # Check for specific email categorization first
    found_categorization = False
    for key in st.session_state.keys():
        if key.startswith("email_to_categorize_"):
            found_categorization = True
            email = st.session_state[key]
            st.subheader(f"Category for: {email['subject']}")
            
            with st.spinner("Categorizing email with Gemini..."):
                category = email_ai.categorize_email(email)
            
            st.write("**AI Category:**")
            st.write(category)
            
            if st.button("Clear Categorization Result"):
                clear_tab_state("email_to_categorize_")
                st.rerun()
            break
    
    if not found_categorization:
        st.info("Select an email from the Email List tab to categorize, or analyze recent emails below.")
        
        if st.button("📊 Analyze Recent Emails"):
            with st.spinner("Analyzing emails with Gemini..."):
                messages = gmail_manager.get_messages(max_results=30)
                
                if messages:
                    categories = []
                    senders = []
                    
                    for msg in messages:
                        email_details = gmail_manager.get_message_details(msg['id'])
                        if email_details:
                            content = gmail_manager.extract_email_content(email_details)
                            
                            # Categorize email
                            category = email_ai.categorize_email(content)
                            categories.append(category)
                            senders.append(content['sender'])
                    
                    # Create analytics
                    st.subheader("Email Categories")
                    category_counts = {}
                    for cat in categories:
                        # Extract category from AI response
                        if "Category:" in cat:
                            category = cat.split("Category:")[1].split("\n")[0].strip()
                            category_counts[category] = category_counts.get(category, 0) + 1
                    
                    if category_counts:
                        df_categories = pd.DataFrame(list(category_counts.items()), 
                                                   columns=['Category', 'Count'])
                        st.bar_chart(df_categories.set_index('Category'))
                    
                    st.subheader("Top Senders")
                    sender_counts = {}
                    for sender in senders:
                        # Extract email from sender
                        sender_email = gmail_manager.extract_sender_email(sender)
                        sender_counts[sender_email] = sender_counts.get(sender_email, 0) + 1
                    
                    # Show top 10 senders
                    top_senders = sorted(sender_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                    df_senders = pd.DataFrame(top_senders, columns=['Sender', 'Count'])
                    st.dataframe(df_senders)


def render_sentiment_tab(email_ai):
    """Render the sentiment analysis tab"""
    st.header("Sentiment Analysis")
    
    found = False
    for key in st.session_state.keys():
        if key.startswith("email_to_analyze_"):
            found = True
            email = st.session_state[key]
            st.subheader(f"Sentiment Analysis for: {email['subject']}")
            
            with st.spinner("Analyzing sentiment with Gemini..."):
                sentiment = email_ai.analyze_sentiment(email)
            
            st.write("**Sentiment Analysis:**")
            st.write(sentiment)
            
            if st.button("Clear Sentiment Result"):
                clear_tab_state("email_to_analyze_")
                st.rerun()
            break
    
    if not found:
        st.info("Select an email from the Email List tab to analyze sentiment.")


def render_chatbot_tab(gmail_manager, rag_chatbot):
    """Render the RAG chatbot tab"""
    st.header("🤖 Email Chatbot")
    st.markdown("Ask questions about your emails and get AI-powered insights!")
    
    # Initialize session state for selected emails
    if 'selected_emails_for_chat' not in st.session_state:
        st.session_state.selected_emails_for_chat = []
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar for email selection
    with st.sidebar:
        st.subheader("📧 Select Emails for Chat")
        
        # Fetch recent emails for selection
        with st.spinner("Loading emails..."):
            messages = gmail_manager.get_messages(max_results=50)
        
        if messages:
            st.write(f"Found {len(messages)} recent emails")
            
            # Email selection interface
            selected_indices = st.multiselect(
                "Choose emails to include in chat context:",
                options=range(len(messages)),
                format_func=lambda x: f"{messages[x]['id'][:8]}...",
                help="Select emails to provide context for the chatbot"
            )
            
            # Load selected emails
            if st.button("🔄 Load Selected Emails"):
                st.session_state.selected_emails_for_chat = []
                for idx in selected_indices:
                    email_details = gmail_manager.get_message_details(messages[idx]['id'])
                    if email_details:
                        content = gmail_manager.extract_email_content(email_details)
                        st.session_state.selected_emails_for_chat.append(content)
                st.success(f"Loaded {len(st.session_state.selected_emails_for_chat)} emails!")
            
            # Show currently loaded emails
            if st.session_state.selected_emails_for_chat:
                st.write(f"**Currently loaded:** {len(st.session_state.selected_emails_for_chat)} emails")
                if st.button("🗑️ Clear Selection"):
                    st.session_state.selected_emails_for_chat = []
                    st.session_state.chat_history = []
                    st.rerun()
        else:
            st.warning("No emails found. Please check your Gmail connection.")
    
    # Main chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat history display
        st.subheader("💬 Chat History")
        
        if st.session_state.chat_history:
            for i, (question, answer) in enumerate(st.session_state.chat_history):
                with st.expander(f"Q: {question[:50]}...", expanded=True):
                    st.write(f"**Question:** {question}")
                    st.write(f"**Answer:** {answer}")
                    if st.button(f"🗑️ Delete", key=f"del_{i}"):
                        st.session_state.chat_history.pop(i)
                        st.rerun()
        else:
            st.info("No chat history yet. Ask a question to get started!")
        
        # Question input
        st.subheader("❓ Ask a Question")
        
        # Handle auto-filled question from suggestions
        default_question = ""
        if 'auto_question' in st.session_state:
            default_question = st.session_state.auto_question
            del st.session_state.auto_question
        
        user_question = st.text_area(
            "Ask anything about your emails:",
            value=default_question,
            placeholder="e.g., What are the main topics in my emails? Who sent me urgent messages?",
            height=100
        )
        
        if st.button("🚀 Ask Question", disabled=not user_question):
            if not st.session_state.selected_emails_for_chat:
                st.error("Please select some emails first in the sidebar!")
            else:
                with st.spinner("Analyzing your emails..."):
                    answer = rag_chatbot.answer_question(user_question, st.session_state.selected_emails_for_chat)
                
                # Add to chat history
                st.session_state.chat_history.append((user_question, answer))
                st.rerun()
    
    with col2:
        # Quick actions and suggestions
        st.subheader("💡 Quick Actions")
        
        if st.button("🔍 Search Emails by Content"):
            search_query = st.text_input("Enter search terms:")
            if search_query and st.session_state.selected_emails_for_chat:
                relevant_emails = rag_chatbot.search_emails_by_content(search_query, st.session_state.selected_emails_for_chat)
                if relevant_emails:
                    st.write(f"Found {len(relevant_emails)} relevant emails:")
                    for email in relevant_emails[:5]:
                        st.write(f"- {email['subject'][:40]}...")
                else:
                    st.info("No relevant emails found.")
        
        if st.button("📊 Analyze Email Patterns"):
            if st.session_state.selected_emails_for_chat:
                with st.spinner("Analyzing patterns..."):
                    analysis = rag_chatbot.analyze_email_patterns(st.session_state.selected_emails_for_chat)
                st.write("**Pattern Analysis:**")
                st.write(analysis)
            else:
                st.warning("Please select emails first!")
        
        # Suggested questions
        st.subheader("💭 Suggested Questions")
        if st.session_state.selected_emails_for_chat:
            suggested_questions = rag_chatbot.suggest_questions(st.session_state.selected_emails_for_chat)
            for i, question in enumerate(suggested_questions):
                if st.button(f"💡 {question[:30]}...", key=f"suggest_{i}"):
                    # Auto-fill the question input
                    st.session_state.auto_question = question
                    st.rerun()
        else:
            st.info("Select emails to get personalized suggestions!")
        



def render_footer():
    """Render the footer"""
    st.markdown("---")
    st.markdown("""
    **Gmail AI Assistant** - Built with Streamlit and Google Gemini 2.0 Flash
    
    **Features:**
    - 📧 Email listing and management
    - 🔍 Smart search with natural language
    - 📝 AI-powered email summaries
    - 💬 Smart reply generation with multiple tones
    - 🏷️ Automatic email categorization
    - 📊 Email analytics and insights
    - ⚡ Action item extraction
    - 🎭 Sentiment analysis
    - 🤖 RAG Chatbot for email queries
    
    **Powered by Google Gemini 2.0 Flash** for advanced AI capabilities
    """) 