"""
Configuration and constants for the Gmail AI Assistant
"""

# Gmail API Scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']

# Search examples for the smart search feature
SEARCH_EXAMPLES = [
    "jobs related emails",
    "emails from LinkedIn",
    "meeting invitations",
    "urgent emails",
    "emails with attachments",
    "newsletters"
]

# Reply tone options
REPLY_TONES = [
    "professional", 
    "friendly", 
    "formal", 
    "casual", 
    "enthusiastic", 
    "apologetic", 
    "urgent"
]

# Email categories for AI classification
EMAIL_CATEGORIES = [
    "Work/Professional",
    "Personal",
    "Jobs/Career",
    "Marketing/Promotional",
    "Newsletter/Updates",
    "Spam/Junk",
    "Finance/Banking",
    "Travel",
    "Education",
    "Other"
]

# App configuration
APP_CONFIG = {
    "page_title": "Gmail AI Assistant - ChatGPT Powered",
    "page_icon": "📧",
    "layout": "wide"
}

# AI Provider Configuration
AI_PROVIDERS = ["OpenAI", "Gemini", "Claude", "Grok"]

# Default AI provider
DEFAULT_AI_PROVIDER = "OpenAI"

# AI Provider Configuration with Available Models
AI_CONFIG = {
    "OpenAI": {
        "api_key_env": "OPENAI_API_KEY",
        "models": [
            {"name": "gpt-4o", "description": "Fastest and most capable model"},
            {"name": "gpt-4-turbo", "description": "Improved version of GPT-4"},
            {"name": "gpt-4", "description": "Most capable model"},
            {"name": "gpt-3.5-turbo", "description": "Balanced performance and cost"}
        ],
        "default_model": "gpt-4o",
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "Gemini": {
        "api_key_env": "GEMINI_API_KEY",
        "models": [
            {"name": "gemini-2.5-flash", "description": "Fast and free model (recommended)"},
            {"name": "gemini-1.5-pro", "description": "Balanced performance"},
            {"name": "gemini-2.0-pro", "description": "Advanced capabilities"},
            {"name": "gemini-1.0-ultra", "description": "Most powerful model"}
        ],
        "default_model": "gemini-2.5-flash",
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "Claude": {
        "api_key_env": "ANTHROPIC_API_KEY",
        "models": [
            {"name": "claude-3-opus-20240229", "description": "Most capable model"},
            {"name": "claude-3-sonnet-20240229", "description": "Balanced performance"},
            {"name": "claude-3-haiku-20240307", "description": "Fast and cost-effective"}
        ],
        "default_model": "claude-3-sonnet-20240229",
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "Grok": {
        "api_key_env": "GROK_API_KEY",
        "models": [
            {"name": "grok-1.5", "description": "Latest model with improved capabilities"},
            {"name": "grok-1.5-vision", "description": "Supports image understanding"},
            {"name": "grok-1", "description": "Original model"}
        ],
        "default_model": "grok-1.5",
        "temperature": 0.7,
        "max_tokens": 1000
    }
}

# Tab names
TAB_NAMES = [
    "📨 Email List", 
    "🔍 Smart Search", 
    "📝 Summaries", 
    "💬 Smart Reply", 
    "📊 Analytics",
    "🎭 Sentiment Analysis",
    "🤖 Email Chatbot"
] 