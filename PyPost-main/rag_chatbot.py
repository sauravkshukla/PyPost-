"""
RAG (Retrieval-Augmented Generation) Chatbot for Email Analysis
"""

import streamlit as st
from typing import List, Dict, Any, Optional
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config import EMAIL_CATEGORIES

class EmailRAGChatbot:
    """RAG Chatbot for querying email content using various AI providers and FAISS"""
    
    def __init__(self, ai_provider):
        """Initialize the RAG Chatbot with an AI provider"""
        self.ai_provider = ai_provider
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.faiss_index = None
        self.email_vectors = None
        self.emails = []
    
    def build_faiss_index(self, emails: List[Dict[str, Any]]):
        """Build a FAISS index for the given emails"""
        self.emails = emails
        if not emails:
            self.faiss_index = None
            self.email_vectors = None
            return
        texts = [f"Subject: {e.get('subject','')}\nBody: {e.get('body','')}" for e in emails]
        vectors = self.embedder.encode(texts, show_progress_bar=False)
        self.email_vectors = np.array(vectors).astype('float32')
        self.faiss_index = faiss.IndexFlatL2(self.email_vectors.shape[1])
        self.faiss_index.add(self.email_vectors)
    
    def search_emails_faiss(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search emails using FAISS semantic search"""
        if not self.faiss_index or not self.emails:
            return []
        query_vec = self.embedder.encode([query]).astype('float32')
        D, I = self.faiss_index.search(query_vec, top_k)
        return [self.emails[i] for i in I[0] if i < len(self.emails)]
    
    def _generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response using the configured AI provider"""
        try:
            return self.ai_provider.generate_response(prompt, **kwargs)
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return f"Sorry, I couldn't generate a response at this time. Error: {str(e)}"
    
    def create_email_context(self, emails: List[Dict[str, Any]]) -> str:
        if not emails:
            return "No emails available for context."
        context_parts = []
        for i, email in enumerate(emails, 1):
            context_parts.append(f"""
Email {i}:
- Subject: {email.get('subject', 'No Subject')}
- From: {email.get('sender', 'Unknown Sender')}
- Date: {email.get('date', 'Unknown Date')}
- Content: {email.get('body', 'No content')}
---""")
        return "\n".join(context_parts)
    
    def answer_question(self, question: str, emails: List[Dict[str, Any]]) -> str:
        if not emails:
            return "No emails are available to answer your question. Please select some emails first."
        # Use FAISS to select the most relevant emails for the question
        self.build_faiss_index(emails)
        relevant_emails = self.search_emails_faiss(question, top_k=min(5, len(emails)))
        context = self.create_email_context(relevant_emails)
        prompt = f"""
You are an AI assistant that helps users understand their emails. You have access to the following email context:

{context}

User Question: {question}

Please provide a comprehensive answer based on the email context above. Your response should:

1. Directly address the user's question
2. Reference specific emails when relevant
3. Provide actionable insights when possible
4. Be clear and concise
5. If the question cannot be answered with the provided context, say so clearly

Answer:"""
        return self._generate_response(prompt)
    
    def suggest_questions(self, emails: List[Dict[str, Any]]) -> List[str]:
        if not emails:
            return [
                "What are the main topics in my recent emails?",
                "Who are the most frequent senders?",
                "Are there any urgent emails I should prioritize?",
                "What meetings or events are mentioned?",
                "Are there any action items I need to follow up on?"
            ]
        self.build_faiss_index(emails[:5])
        context = self.create_email_context(emails[:5])
        prompt = f"""
Based on these emails:

{context}

Generate 5 relevant questions that a user might want to ask about these emails. 
Focus on practical, actionable questions that would help someone understand and manage their emails better.

Format as a simple list, one question per line:"""
        response = self._generate_response(prompt)
        questions = [q.strip() for q in response.split('\n') if q.strip() and '?' in q]
        if not questions:
            questions = [
                "What are the main topics in these emails?",
                "Who are the key senders and what do they want?",
                "Are there any deadlines or urgent matters mentioned?",
                "What meetings or events are scheduled?",
                "Are there any action items I need to address?"
            ]
        return questions[:5]
    
    def analyze_email_patterns(self, emails: List[Dict[str, Any]]) -> str:
        if not emails:
            return "No emails selected for analysis."
        context = self.create_email_context(emails)
        prompt = f"""
Analyze the following emails and provide insights about:

1. Common themes or topics
2. Sender patterns and relationships
3. Urgency levels and priorities
4. Action items and deadlines
5. Communication patterns and tone

Email Context:
{context}

Please provide a structured analysis with clear sections."""
        return self._generate_response(prompt)
    
    def search_emails_by_content(self, query: str, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not emails:
            return []
        self.build_faiss_index(emails)
        return self.search_emails_faiss(query, top_k=10) 