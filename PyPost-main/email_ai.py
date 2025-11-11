"""
Email AI module for handling AI-powered email operations using various AI providers
"""

import streamlit as st
from config import EMAIL_CATEGORIES, AI_CONFIG

class EmailAI:
    """Handles AI-powered email operations using various AI providers"""
    
    def __init__(self, ai_provider):
        """Initialize EmailAI with an AI provider"""
        self.ai_provider = ai_provider
        
    def _generate_response(self, prompt, **kwargs):
        """Generate response using the configured AI provider"""
        try:
            return self.ai_provider.generate_response(prompt, **kwargs)
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return f"Sorry, I couldn't generate a response at this time. Error: {str(e)}"
    
    def summarize_email(self, email_content):
        """Summarize an email"""
        prompt = f"""
        Please provide a concise summary of this email:
        
        Subject: {email_content['subject']}
        From: {email_content['sender']}
        Date: {email_content['date']}
        
        Content: {email_content['body']}
        
        Summary should include:
        1. Main topic/purpose
        2. Key points
        3. Action items (if any)
        4. Urgency level (Low/Medium/High)
        
        Please format the summary clearly and concisely.
        """
        
        return self._generate_response(prompt)
    
    def generate_smart_reply(self, email_content, reply_tone="professional"):
        """Generate a smart reply to an email"""
        prompt = f"""
        Generate a {reply_tone} reply to this email:
        
        Original Email:
        Subject: {email_content['subject']}
        From: {email_content['sender']}
        Date: {email_content['date']}
        Content: {email_content['body']}
        
        Please write a thoughtful and appropriate response that:
        1. Acknowledges the sender's message
        2. Addresses their main points
        3. Provides a clear response
        4. Maintains a {reply_tone} tone
        5. Is concise but complete
        
        Do not include subject line or sender information in the response, just the email body.
        """
        
        return self._generate_response(prompt)
    
    def categorize_email(self, email_content):
        """Categorize an email"""
        categories_str = "\n".join([f"- {cat}" for cat in EMAIL_CATEGORIES])
        
        prompt = f"""
        Categorize this email into one of these categories:
        {categories_str}
        
        Also provide a confidence score (0-100) for your categorization and a brief explanation.
        
        Email Content:
        Subject: {email_content['subject']}
        From: {email_content['sender']}
        Content: {email_content['body'][:500]}...
        
        Format your response as: 
        Category: [category]
        Confidence: [score]%
        Explanation: [brief explanation]
        """
        
        return self._generate_response(prompt)
    
    def extract_action_items(self, email_content):
        """Extract action items from an email"""
        prompt = f"""
        Extract action items from this email. For each action item, provide:
        1. What needs to be done
        2. Who is responsible (if mentioned)
        3. Deadline (if mentioned)
        4. Priority level (High/Medium/Low)
        
        Email Content:
        Subject: {email_content['subject']}
        From: {email_content['sender']}
        Content: {email_content['body']}
        
        If no action items are found, respond with "No action items found."
        
        Format each action item clearly with bullet points.
        """
        
        return self._generate_response(prompt)
    
    def analyze_sentiment(self, email_content):
        """Analyze the sentiment of an email"""
        prompt = f"""
        Analyze the sentiment and tone of this email:
        
        Subject: {email_content['subject']}
        From: {email_content['sender']}
        Content: {email_content['body']}
        
        Provide:
        1. Overall sentiment (Positive/Negative/Neutral)
        2. Tone (Formal/Informal/Friendly/Urgent/etc.)
        3. Confidence level (0-100%)
        4. Key emotional indicators
        
        Format your response clearly.
        """
        
        return self._generate_response(prompt)
    
    def generate_search_query(self, natural_query):
        """Convert natural language query to Gmail search query"""
        prompt = f"""
        Convert this natural language query to a Gmail search query:
        
        Natural Query: {natural_query}
        
        Convert it to Gmail's search syntax. Common patterns:
        - Jobs/Career: from:(linkedin.com OR indeed.com OR glassdoor.com) OR subject:(job OR career OR opportunity OR hiring)
        - Meetings: subject:(meeting OR call OR zoom OR teams)
        - Urgent: subject:(urgent OR important OR ASAP)
        - Newsletters: subject:(newsletter OR update OR digest)
        
        Return only the Gmail search query, nothing else.
        """
        
        return self._generate_response(prompt) 