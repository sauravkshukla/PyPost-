#!/usr/bin/env python3
"""
SSL Issue Fix Script for Gmail AI Assistant
Run this script to fix common SSL/TLS issues
"""

import subprocess
import sys
import os
import ssl
import socket
import requests

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Check Python version"""
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 7):
        print("⚠️  Warning: Python 3.7+ is recommended")
    else:
        print("✅ Python version is compatible")

def check_ssl_version():
    """Check SSL version"""
    print(f"OpenSSL version: {ssl.OPENSSL_VERSION}")
    try:
        print(f"SSL version info: {ssl.version_info}")
    except AttributeError:
        print("SSL version info: Not available")

def update_packages():
    """Update Python packages"""
    print("\n🔄 Updating Python packages...")
    
    # Update pip
    success, stdout, stderr = run_command(f"{sys.executable} -m pip install --upgrade pip")
    if success:
        print("✅ pip updated successfully")
    else:
        print(f"❌ Failed to update pip: {stderr}")
    
    # Update requirements
    if os.path.exists('requirements.txt'):
        success, stdout, stderr = run_command(f"{sys.executable} -m pip install --upgrade -r requirements.txt")
        if success:
            print("✅ Requirements updated successfully")
        else:
            print(f"❌ Failed to update requirements: {stderr}")
    else:
        print("⚠️  requirements.txt not found")

def test_network_connectivity():
    """Test network connectivity"""
    print("\n🌐 Testing network connectivity...")
    
    try:
        response = requests.get('https://www.google.com', timeout=10)
        if response.status_code == 200:
            print("✅ Internet connection is working")
            return True
        else:
            print(f"❌ Internet connection failed (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Internet connection failed: {str(e)}")
        return False

def test_gmail_api():
    """Test Gmail API access"""
    print("\n📧 Testing Gmail API access...")
    
    try:
        response = requests.get('https://gmail.googleapis.com/gmail/v1/users/me/profile', timeout=10)
        if response.status_code in [200, 401, 403]:
            print("✅ Gmail API is accessible")
            return True
        else:
            print(f"❌ Gmail API access failed (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Gmail API access failed: {str(e)}")
        return False

def clear_auth_cache():
    """Clear authentication cache"""
    print("\n🗑️  Clearing authentication cache...")
    
    if os.path.exists('token.pickle'):
        try:
            os.remove('token.pickle')
            print("✅ Authentication cache cleared")
        except Exception as e:
            print(f"❌ Failed to clear cache: {str(e)}")
    else:
        print("ℹ️  No authentication cache found")

def check_credentials():
    """Check if credentials file exists"""
    print("\n🔑 Checking credentials...")
    
    if os.path.exists('credentials.json'):
        print("✅ credentials.json found")
        return True
    else:
        print("❌ credentials.json not found")
        print("   Please download your Gmail API credentials from Google Cloud Console")
        return False

def main():
    """Main function"""
    print("🔧 SSL Issue Fix Script for Gmail AI Assistant")
    print("=" * 50)
    
    # Check Python and SSL
    check_python_version()
    check_ssl_version()
    
    # Update packages
    update_packages()
    
    # Test connectivity
    network_ok = test_network_connectivity()
    gmail_ok = test_gmail_api()
    
    # Clear cache
    clear_auth_cache()
    
    # Check credentials
    credentials_ok = check_credentials()
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print(f"   Network connectivity: {'✅' if network_ok else '❌'}")
    print(f"   Gmail API access: {'✅' if gmail_ok else '❌'}")
    print(f"   Credentials file: {'✅' if credentials_ok else '❌'}")
    
    if network_ok and gmail_ok and credentials_ok:
        print("\n🎉 All checks passed! Try running the app again.")
    else:
        print("\n⚠️  Some issues detected. Please check the troubleshooting guide in README.md")
    
    print("\n💡 Next steps:")
    print("   1. Run: streamlit run app.py")
    print("   2. If issues persist, check the troubleshooting section in README.md")
    print("   3. Try disabling VPN or firewall temporarily")

if __name__ == "__main__":
    main() 