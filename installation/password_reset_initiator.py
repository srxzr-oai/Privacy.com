#!/usr/bin/env python3
"""
Privacy.com Password Reset Initiator
This script initiates the password reset process by sending a reset request to Privacy.com
"""

import requests
import json
import sys
import time
from datetime import datetime
from config import PRIVACY_COM_URLS, DEFAULT_HEADERS, REQUEST_TIMEOUT


class PasswordResetInitiator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        
    def initiate_reset(self, email):
        """
        Initiate password reset for the given email address
        
        Args:
            email (str): The Gmail address for password reset
            
        Returns:
            dict: Response data from the password reset request
        """
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Initiating password reset for: {email}")
        
        try:
            reset_data = {
                "email": email,
                "login_url": PRIVACY_COM_URLS["login_redirect"]
            }
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sending reset request to Privacy.com...")
            
            response = self.session.post(
                PRIVACY_COM_URLS["password_reset"],
                json=reset_data,
                timeout=REQUEST_TIMEOUT
            )
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Password reset initiated successfully!")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Check your email for reset instructions")
                
                # Save session info for the next step
                self.save_session_info(email, result)
                return result
                
            elif response.status_code == 429:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Rate limited. Please wait before trying again")
                return None
                
            elif response.status_code == 404:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Email not found in Privacy.com system")
                return None
                
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Unexpected response: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Request timed out")
            return None
            
        except requests.exceptions.ConnectionError:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Connection error")
            return None
            
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error: {str(e)}")
            return None
    
    def save_session_info(self, email, response_data):
        """Save session information for use in the next step"""
        session_info = {
            "email": email,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data,
            "cookies": dict(self.session.cookies)
        }
        
        with open("session_info.json", "w") as f:
            json.dump(session_info, f, indent=2)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Session info saved to session_info.json")


def main():
    if len(sys.argv) != 2:
        print("Usage: python password_reset_initiator.py <email@gmail.com|email@openai.com>")
        print("Example: python password_reset_initiator.py john.doe@gmail.com")
        print("Example: python password_reset_initiator.py john.doe@openai.com")
        sys.exit(1)
    
    email = sys.argv[1].strip()
    
    if not (email.endswith("@gmail.com") or email.endswith("@openai.com")):
        print("❌ Please provide a Gmail (@gmail.com) or OpenAI (@openai.com) address")
        sys.exit(1)
    
    if "@" not in email or "." not in email:
        print("❌ Please provide a valid email address")
        sys.exit(1)
    
    print("=" * 60)
    print("Privacy.com Password Reset Initiator")
    print("=" * 60)
    
    initiator = PasswordResetInitiator()
    result = initiator.initiate_reset(email)
    
    if result:
        print("\n" + "=" * 60)
        print("✅ NEXT STEPS:")
        print("1. Check your Gmail inbox for the reset email")
        print("2. Look for the temporary reset code in the email")
        print("3. Run: python password_reset_verifier.py <temporary_code>")
        print("=" * 60)
    else:
        print("\n❌ Password reset initiation failed. Please try again.")


if __name__ == "__main__":
    main() 