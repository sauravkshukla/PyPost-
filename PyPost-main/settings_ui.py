"""
Settings UI Module
Handles the user interface for application settings including AI provider selection.
"""
import streamlit as st
from config import AI_PROVIDERS, AI_CONFIG, DEFAULT_AI_PROVIDER

def show_ai_settings():
    """Display AI provider selection and API key input in the sidebar."""
    with st.sidebar:
        st.header("🔧 AI Settings")
        
        # Gmail Authentication
        st.markdown("---")
        st.markdown("### 📧 Gmail Authentication")
        if st.button("Connect Gmail Account", type="primary"):
            st.session_state.gmail_auth_in_progress = True
            st.rerun()
        
        if st.session_state.get('gmail_auth_in_progress', False):
            st.info("Please check your browser for the Gmail authentication window.")
            
        if st.session_state.get('gmail_authenticated', False):
            st.success("✅ Successfully connected to Gmail")
            st.button("Disconnect Gmail", type="secondary", on_click=lambda: st.session_state.update({
                'gmail_authenticated': False,
                'gmail_auth_in_progress': False
            }))
        
        st.markdown("---")
        st.header("🔧 AI Settings")
        
        # Initialize session state for AI provider if not exists
        if 'selected_ai_provider' not in st.session_state:
            st.session_state.selected_ai_provider = DEFAULT_AI_PROVIDER
        
        # AI Provider Selection with icons
        provider_icons = {
            "OpenAI": "🤖",
            "Gemini": "🔮",
            "Claude": "👾",
            "Grok": "🚀"
        }
        
        # Display provider selection as buttons
        st.markdown("### Select AI Provider")
        cols = st.columns(2)
        for i, provider in enumerate(AI_PROVIDERS):
            with cols[i % 2]:
                if st.button(f"{provider_icons.get(provider, '📌')} {provider}", 
                           key=f"btn_{provider}",
                           use_container_width=True,
                           type="primary" if st.session_state.selected_ai_provider == provider else "secondary"):
                    st.session_state.selected_ai_provider = provider
                    st.rerun()
        
        selected_provider = st.session_state.selected_ai_provider
        st.markdown("---")
        
        # API Key Input
        st.markdown(f"### {selected_provider} Settings")
        
        # Get or initialize API key in session state
        api_key_env = AI_CONFIG[selected_provider]["api_key_env"]
        if f"{api_key_env}_input" not in st.session_state:
            st.session_state[f"{api_key_env}_input"] = ""
        
        # API Key Input with better styling
        api_key = st.text_input(
            "🔑 API Key",
            type="password",
            value=st.session_state[f"{api_key_env}_input"],
            help=f"Enter your {selected_provider} API key",
            placeholder=f"sk-..." if selected_provider == "OpenAI" else "Your API key here"
        )
        
        # Save API key to session state
        if api_key != st.session_state[f"{api_key_env}_input"]:
            st.session_state[f"{api_key_env}_input"] = api_key
            st.session_state[f"{selected_provider.upper()}_API_KEY"] = api_key
            st.success(f"✅ {selected_provider} API key saved")
        
        # Model selection in an expander
        with st.expander("⚙️ Advanced Settings", expanded=False):
            # Get available models from config
            if 'models' in AI_CONFIG[selected_provider]:
                models = AI_CONFIG[selected_provider]['models']
                default_model = AI_CONFIG[selected_provider].get('default_model')
                
                # Create model selection dropdown with descriptions
                model_options = [f"{m['name']} - {m['description']}" for m in models]
                model_values = [m['name'] for m in models]
                
                # Find index of default model
                default_index = model_values.index(default_model) if default_model in model_values else 0
                
                # Display model selection with descriptions
                selected_model_display = st.selectbox(
                    "🤖 Model",
                    options=model_options,
                    index=default_index,
                    key=f"{selected_provider}_model_select_display",
                    help="Select the AI model to use for this provider"
                )
                
                # Get the actual model name without description
                selected_model = model_values[model_options.index(selected_model_display)]
                st.session_state['selected_model'] = selected_model
                
                # Show model info
                st.caption(f"Selected model: `{selected_model}`")
            
            # Additional settings for OpenAI
            if selected_provider == 'OpenAI':
                st.slider(
                    "🌡️ Temperature",
                    min_value=0.0,
                    max_value=2.0,
                    value=0.7,
                    step=0.1,
                    key="temperature_setting",
                    help="Higher values make the output more random, lower values more deterministic."
                )
                
                st.slider(
                    "📏 Max Tokens",
                    min_value=100,
                    max_value=4000,
                    value=1000,
                    step=100,
                    key="max_tokens_setting",
                    help="Maximum number of tokens to generate in the response."
                )
        
        # Documentation links in an expander
        with st.expander("📚 API Key Help", expanded=False):
            st.markdown("### Get API Keys")
            docs_links = {
                "OpenAI": "https://platform.openai.com/api-keys",
                "Gemini": "https://aistudio.google.com/app/apikey",
                "Claude": "https://console.anthropic.com/settings/keys",
                "Grok": "https://x.ai/"
            }
            
            st.markdown("Click below to get your API key:")
            for provider, url in docs_links.items():
                st.markdown(f"- [{provider} API Key]({url})")
            
            st.markdown("\n**Note:** Your API key is stored only in your browser session and is never sent to our servers.")

def get_ai_settings():
    """Get the current AI settings from session state."""
    provider = st.session_state.get('selected_ai_provider', DEFAULT_AI_PROVIDER)
    api_key = st.session_state.get(f"{AI_CONFIG[provider]['api_key_env']}_input", "")
    
    # Get the selected model or use the default from config
    selected_model = st.session_state.get('selected_model')
    if not selected_model and 'models' in AI_CONFIG[provider]:
        selected_model = AI_CONFIG[provider].get('default_model')
    elif not selected_model:
        selected_model = AI_CONFIG[provider].get('model', '')
    
    return {
        'provider': provider,
        'api_key': api_key,
        'model': selected_model,
        'temperature': st.session_state.get('temperature_setting', 0.7),
        'max_tokens': st.session_state.get('max_tokens_setting', 1000)
    }
