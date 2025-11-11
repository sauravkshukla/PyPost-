# Gmail AI Assistant

A powerful Gmail assistant powered by Google Gemini AI that helps you manage, analyze, and respond to emails intelligently.

## 🚀 Features

- 📧 **Email Management**: List and view recent emails
- 🔍 **Smart Search**: Natural language search with AI-powered query conversion
- 📝 **AI Summaries**: Get concise summaries of emails with key points and action items
- 💬 **Smart Replies**: Generate contextual replies with multiple tone options
- 🏷️ **Email Categorization**: Automatically categorize emails by type
- 📊 **Analytics**: Visual insights into email patterns and sender statistics
- 🎭 **Sentiment Analysis**: Analyze email tone and sentiment
- ⚡ **Action Item Extraction**: Automatically identify tasks and deadlines
- 🤖 **RAG Chatbot**: Ask questions about your emails and get AI-powered insights

## 🏗️ Architecture

The application has been refactored into modular components for better maintainability:

### 📁 Project Structure

```
ai_mail/
├── app.py              # Main application entry point
├── config.py           # Configuration and constants
├── gmail_manager.py    # Gmail API operations
├── email_ai.py         # AI/ML functionality using Gemini
├── rag_chatbot.py      # RAG chatbot for email queries
├── ui_components.py    # Streamlit UI components
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
├── credentials.json   # Gmail API credentials (not tracked)
└── token.pickle       # Authentication token (not tracked)
```

### 🔧 Module Responsibilities

- **`app.py`**: Main application orchestrator, handles tab navigation and session management
- **`config.py`**: Centralized configuration including API scopes, UI constants, and search examples
- **`gmail_manager.py`**: Handles all Gmail API operations (authentication, fetching emails, sending replies)
- **`email_ai.py`**: AI-powered email operations using Google Gemini (summaries, replies, categorization, sentiment analysis)
- **`rag_chatbot.py`**: RAG chatbot for querying email content with context-aware responses
- **`ui_components.py`**: Reusable Streamlit UI components separated by functionality

## 🛠️ Setup Instructions

### Prerequisites

1. **Google Gemini API Key**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Gmail API Credentials**: Download `credentials.json` from [Google Cloud Console](https://console.cloud.google.com/)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Place your credentials**:
   - Put your `credentials.json` file in the project directory
   - The file is already in `.gitignore` for security

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **First-time setup**:
   - Enter your Gemini API key in the sidebar
   - Click "Authenticate with Gmail" to authorize the application
   - Follow the browser authentication flow

## 🔐 Security

- `credentials.json` and `token.pickle` are excluded from version control
- API keys are handled securely through Streamlit's password input
- Authentication tokens are stored locally and refreshed automatically

## 🔧 Troubleshooting

### SSL/TLS Issues

If you encounter SSL errors like `SSLError: [SSL: WRONG_VERSION_NUMBER]`, try these solutions:

1. **Update Python and packages**:
   ```bash
   pip install --upgrade pip
   pip install --upgrade -r requirements.txt
   ```

2. **Check your network connection**:
   - Use the Network Diagnostics section in the app
   - Test internet connectivity
   - Verify Gmail API access

3. **Network/Firewall issues**:
   - Disable VPN temporarily
   - Check firewall settings
   - Try a different network connection

4. **System-specific solutions**:
   - **Windows**: Update Windows and check proxy settings
   - **macOS**: Update system certificates: `sudo /usr/bin/security find-certificate -a -p /System/Library/Keychains/SystemRootCertificates.keychain > ~/.ssl/cert.pem`
   - **Linux**: Update CA certificates: `sudo update-ca-certificates`

5. **Clear authentication cache**:
   - Delete `token.pickle` file
   - Re-authenticate with Gmail

### Common Issues

- **"credentials.json not found"**: Download your Gmail API credentials from Google Cloud Console
- **"Authentication failed"**: Check your credentials.json file and ensure Gmail API is enabled
- **"Network connectivity failed"**: Check your internet connection and firewall settings

## 🎯 Usage

### Email List Tab
- View recent emails with expandable details
- Use action buttons to summarize, reply, categorize, or analyze emails

### Smart Search Tab
- Choose from predefined search examples or enter custom queries
- AI converts natural language to Gmail search syntax

### Summaries Tab
- View AI-generated summaries of selected emails
- Extract action items and key points automatically

### Smart Reply Tab
- Generate contextual replies with different tones
- Send replies directly from the application

### Analytics Tab
- Analyze email categories and sender patterns
- View visual charts and statistics

### Sentiment Analysis Tab
- Analyze email tone and sentiment
- Get confidence scores and emotional indicators

### Email Chatbot Tab
- Select multiple emails to provide context
- Ask natural language questions about your emails
- Get AI-powered insights and analysis
- Search emails by content relevance
- View suggested questions based on your email context
- Analyze patterns across multiple emails

## 🚀 Benefits of Refactoring

### ✅ Improved Maintainability
- **Separation of Concerns**: Each module has a single responsibility
- **Reduced Complexity**: Main app.py is now only ~50 lines vs 600+ lines
- **Easier Testing**: Individual components can be tested in isolation

### ✅ Better Code Organization
- **Configuration Management**: All constants centralized in `config.py`
- **UI Reusability**: UI components can be reused and modified independently
- **Clear Dependencies**: Each module's dependencies are explicit

### ✅ Enhanced Development Experience
- **Faster Development**: Work on specific features without navigating large files
- **Easier Debugging**: Issues can be isolated to specific modules
- **Better Collaboration**: Multiple developers can work on different modules

### ✅ Scalability
- **Easy Feature Addition**: New features can be added as separate modules
- **Modular Architecture**: Components can be swapped or extended independently
- **Configuration Flexibility**: Easy to modify settings without touching core logic

## 🔧 Customization

### Adding New Features
1. Create new functions in appropriate modules
2. Add UI components to `ui_components.py`
3. Update `app.py` to include new tabs or functionality
4. Add any new constants to `config.py`

### Modifying AI Prompts
- Edit prompt templates in `email_ai.py`
- All AI functionality is centralized for easy updates

### UI Customization
- Modify UI components in `ui_components.py`
- Update constants in `config.py` for text and options

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests. 