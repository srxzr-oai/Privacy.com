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
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Please initiate password reset using your browser:")
        print("")
        print("📱 BROWSER REQUEST REQUIRED")
        print("=" * 60)
        
        # Construct the reset URL with parameters
        reset_url = f"{PRIVACY_COM_URLS['password_reset']}?email={email}&login_url={PRIVACY_COM_URLS['login_redirect']}"
        
        print(f"🌐 Open this URL in your browser:")
        print(f"   {reset_url}")
        print("")
        print("📋 Instructions:")
        print("1. Copy the URL above")
        print("2. Open it in your web browser (Chrome, Safari, Firefox, etc.)")
        print("3. Copy the entire JSON response from the browser")
        print("4. Paste it below")
        print("")
        
        if email.endswith('@openai.com'):
            print("💡 OpenAI Employee with ChatGPT Agent:")
            print("If you're using a ChatGPT agent, ask it to:")
            print("- Open the URL in browser")
            print("- Copy the JSON response")
            print("- Provide the response back to you")
            print("")
        
        print("=" * 60)
        
        # Get the JSON response from user
        while True:
            print(f"Please paste the JSON response from: {reset_url}")
            user_response = input("JSON Response: ").strip()
            
            if not user_response:
                print("❌ Response cannot be empty. Please try again.")
                continue
            
            try:
                # Parse the JSON response
                import json
                response_data = json.loads(user_response)
                
                # Check if the response indicates success
                if response_data.get("success", False) or response_data.get("status") == "success":
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Password reset initiated successfully!")
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Check your email for reset instructions")
                    
                    # Save session info for the next step
                    self.save_session_info(email, response_data)
                    return response_data
                else:
                    error_msg = response_data.get("error", "Unknown error")
                    status_code = response_data.get("status_code", 0)
                    
                    if status_code == 429:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Rate limited. Please wait before trying again")
                    elif status_code == 404:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Email not found in Privacy.com system")
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Password reset failed: {error_msg}")
                    
                    return None
                    
            except json.JSONDecodeError:
                print("❌ Invalid JSON response. Please make sure you copied the entire JSON response from the browser.")
                print("The response should look like: {\"success\": true, \"email\": \"...\", ...}")
                print("Please try again.")
                continue
    
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