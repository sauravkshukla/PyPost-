"""
Gmail API Manager for handling email operations
"""

import base64
import pickle
import os
import ssl
import socket
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st
from config import SCOPES


class GmailManager:
    """Manages Gmail API operations including authentication, fetching emails, and sending replies"""
    
    def __init__(self):
        self.service = None
        self.creds = None
        
    def authenticate(self):
        """Authenticate with Gmail API"""
        try:
            # Check if credentials.json exists
            if not os.path.exists('credentials.json'):
                st.error("""
                Missing credentials.json file!
                Please download it from Google Cloud Console:
                1. Go to https://console.cloud.google.com/
                2. Create or select your project
                3. Enable Gmail API
                4. Create credentials (OAuth 2.0 Client IDs)
                5. Download credentials.json and place it in the app directory
                """)
                return False

            # Load or create credentials
            creds = None
            if os.path.exists('token.pickle'):
                try:
                    with open('token.pickle', 'rb') as token:
                        creds = pickle.load(token)
                except Exception as e:
                    st.warning(f"Could not load token: {str(e)}")
                    os.remove('token.pickle')  # Remove invalid token

            # If no valid credentials, start OAuth flow
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except Exception as e:
                        st.error(f"Error refreshing credentials: {str(e)}")
                        os.remove('token.pickle')  # Remove invalid token
                        creds = None
                else:
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials.json', SCOPES)
                        flow.redirect_uri = 'http://localhost:8080'
                        creds = flow.run_local_server(port=8080)
                        
                        # Save credentials
                        try:
                            with open('token.pickle', 'wb') as token:
                                pickle.dump(creds, token)
                        except Exception as e:
                            st.warning(f"Could not save credentials: {str(e)}")
                    except Exception as e:
                        st.error(f"Error during authentication flow: {str(e)}")
                        return False

            if not creds:
                st.error("Failed to obtain valid credentials.")
                return False

            self.creds = creds
            
            # Build Gmail service
            try:
                self.service = build('gmail', 'v1', credentials=creds)
                return True
            except Exception as e:
                st.error(f"Error building Gmail service: {str(e)}")
                return False
                
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return False
    
    def get_messages(self, query='', max_results=10):
        """Get messages from Gmail"""
        try:
            if not self.service:
                st.error("Gmail service not initialized. Please authenticate first.")
                return []
            
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=max_results).execute()
            messages = results.get('messages', [])
            return messages
        except HttpError as error:
            st.error(f'Gmail API error: {error}')
            return []
        except Exception as e:
            st.error(f'Unexpected error getting messages: {str(e)}')
            return []
    
    def get_message_details(self, msg_id):
        """Get detailed message content"""
        try:
            if not self.service:
                st.error("Gmail service not initialized. Please authenticate first.")
                return None
            
            message = self.service.users().messages().get(
                userId='me', id=msg_id).execute()
            return message
        except HttpError as error:
            st.error(f'Gmail API error: {error}')
            return None
        except Exception as e:
            st.error(f'Unexpected error getting message details: {str(e)}')
            return None
    
    def extract_email_content(self, message):
        """Extract email content from message"""
        headers = message['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
        
        # Extract body
        body = self._extract_body(message['payload'])
        
        return {
            'id': message['id'],
            'subject': subject,
            'sender': sender,
            'date': date,
            'body': body,
            'thread_id': message['threadId']
        }
    
    def _extract_body(self, payload):
        """Extract email body from payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        else:
            if payload['mimeType'] == 'text/plain':
                if 'data' in payload['body']:
                    body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        return body
    
    def send_reply(self, thread_id, to_email, subject, body):
        """Send a reply to an email"""
        try:
            if not self.service:
                st.error("Gmail service not initialized. Please authenticate first.")
                return None
            
            message = {
                'raw': base64.urlsafe_b64encode(
                    f'To: {to_email}\r\n'
                    f'Subject: Re: {subject}\r\n'
                    f'In-Reply-To: {thread_id}\r\n'
                    f'References: {thread_id}\r\n'
                    f'\r\n'
                    f'{body}'.encode('utf-8')
                ).decode('utf-8')
            }
            
            result = self.service.users().messages().send(
                userId='me', body=message).execute()
            return result
        except HttpError as error:
            st.error(f'Gmail API error: {error}')
            return None
        except Exception as e:
            st.error(f'Unexpected error sending reply: {str(e)}')
            return None
    
    def extract_sender_email(self, sender):
        """Extract email address from sender string"""
        if '<' in sender and '>' in sender:
            return sender.split('<')[1].split('>')[0]
        return sender 