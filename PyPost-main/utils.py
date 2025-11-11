"""
Utility functions for handling SSL and network issues
"""

import ssl
import socket
import urllib3
import requests
from urllib3.util.ssl_ import create_urllib3_context
import streamlit as st


def configure_ssl_context():
    """Configure SSL context to handle various SSL issues"""
    try:
        # Create a custom SSL context
        ssl_context = ssl.create_default_context()
        
        # Set minimum TLS version
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        
        # Allow modern cipher suites
        ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')
        
        # Disable certificate verification for development (use with caution)
        # ssl_context.check_hostname = False
        # ssl_context.verify_mode = ssl.CERT_NONE
        
        return ssl_context
    except Exception as e:
        st.warning(f"Could not configure SSL context: {str(e)}")
        return None


def test_network_connectivity():
    """Test basic network connectivity"""
    try:
        # Test basic internet connectivity
        response = requests.get('https://www.google.com', timeout=10)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Network connectivity test failed: {str(e)}")
        return False


def check_gmail_api_access():
    """Check if Gmail API is accessible"""
    try:
        # Test Gmail API endpoint
        response = requests.get('https://gmail.googleapis.com/gmail/v1/users/me/profile', timeout=10)
        return response.status_code in [200, 401, 403]  # 401/403 means API is reachable but needs auth
    except Exception as e:
        st.error(f"Gmail API access test failed: {str(e)}")
        return False


def get_network_info():
    """Get network information for debugging"""
    try:
        info = {
            'hostname': socket.gethostname(),
            'ssl_version': ssl.OPENSSL_VERSION,
            'python_ssl_version': ssl.version_info,
        }
        return info
    except Exception as e:
        return {'error': str(e)}


def handle_ssl_error(error):
    """Handle SSL errors with specific solutions"""
    error_str = str(error).lower()
    
    if 'wrong_version_number' in error_str:
        return {
            'type': 'SSL_VERSION_ERROR',
            'message': 'SSL/TLS version mismatch. This usually happens when connecting to a non-SSL port with SSL.',
            'solutions': [
                'Check if you\'re using the correct port (443 for HTTPS)',
                'Verify your network proxy settings',
                'Try disabling any VPN or firewall temporarily',
                'Update your Python SSL libraries'
            ]
        }
    elif 'certificate_verify_failed' in error_str:
        return {
            'type': 'SSL_CERT_ERROR',
            'message': 'SSL certificate verification failed.',
            'solutions': [
                'Update your system\'s CA certificates',
                'Check your system clock (certificates depend on correct time)',
                'Try updating Python and pip packages'
            ]
        }
    elif 'connection_refused' in error_str:
        return {
            'type': 'CONNECTION_REFUSED',
            'message': 'Connection was refused by the server.',
            'solutions': [
                'Check your internet connection',
                'Verify the API endpoint is correct',
                'Try again in a few minutes (server might be temporarily unavailable)'
            ]
        }
    else:
        return {
            'type': 'UNKNOWN_SSL_ERROR',
            'message': f'Unknown SSL error: {error}',
            'solutions': [
                'Check your internet connection',
                'Try restarting the application',
                'Update your Python packages',
                'Check for firewall or proxy issues'
            ]
        } 