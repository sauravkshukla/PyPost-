"""
AI Provider Module
Handles initialization and configuration of different AI providers.
"""
import os
import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import anthropic

def get_ai_provider(provider_name=None):
    """
    Get the configured AI provider based on user selection.
    """
    import os
    import streamlit as st
    
    if provider_name is None:
        provider_name = st.session_state.get('selected_ai_provider', 'OpenAI')
    
    # Check session state first, then environment variables
    api_key = st.session_state.get(f"{provider_name.upper()}_API_KEY")
    if not api_key:
        api_key = os.getenv(f"{provider_name.upper()}_API_KEY")
    
    # If still no key, check for a .env file
    if not api_key:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv(f"{provider_name.upper()}_API_KEY")
    
    if not api_key or api_key.startswith('your_'):
        st.warning(f"Please set the {provider_name} API key in the settings.")
        return None
    
    return AIProvider(provider_name, api_key)

class AIProvider:
    def __init__(self, provider_name, api_key):
        self.provider_name = provider_name
        self.api_key = api_key
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate client based on the provider."""
        if self.provider_name == 'OpenAI':
            return OpenAI(api_key=self.api_key)
        elif self.provider_name == 'Gemini':
            genai.configure(api_key=self.api_key)
            return genai
        elif self.provider_name == 'Claude':
            return anthropic.Client(api_key=self.api_key)
        elif self.provider_name == 'Grok':
            # Note: Grok API integration would go here
            # This is a placeholder as Grok's API details may vary
            return {"api_key": self.api_key}
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider_name}")
    
    def generate_response(self, prompt, **kwargs):
        """Generate a response using the selected AI provider."""
        if self.provider_name == 'OpenAI':
            response = self.client.chat.completions.create(
                model=kwargs.get('model', 'gpt-4'),
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 1000)
            )
            return response.choices[0].message.content
            
        elif self.provider_name == 'Gemini':
            model = self.client.GenerativeModel(kwargs.get('model', 'gemini-pro'))
            response = model.generate_content(prompt)
            return response.text
            
        elif self.provider_name == 'Claude':
            response = self.client.messages.create(
                model=kwargs.get('model', 'claude-3-opus-20240229'),
                max_tokens=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.7),
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
            
        elif self.provider_name == 'Grok':
            # Placeholder for Grok API implementation
            return f"[Grok response for: {prompt}]"
            
        return "Error: Unsupported AI provider"
