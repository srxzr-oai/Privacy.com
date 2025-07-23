#!/usr/bin/env python3
"""
Privacy.com Security Code Verifier
This script verifies the temporary security code and completes the security verification process
"""

import requests
import json
import sys
import getpass
from datetime import datetime
from config import PRIVACY_COM_URLS, DEFAULT_HEADERS, REQUEST_TIMEOUT


class SecurityCodeVerifier:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.session_info = None
        
    def load_session_info(self):
        """Load session information from the previous step"""
        try:
            with open("session_info.json", "r") as f:
                self.session_info = json.load(f)
            
            # Restore cookies from previous session
            for name, value in self.session_info.get("cookies", {}).items():
                self.session.cookies.set(name, value)
                
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Session info loaded for: {self.session_info['email']}")
            return True
            
        except FileNotFoundError:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ session_info.json not found")
            print("Please run security_code_initiator.py first")
            return False
            
        except json.JSONDecodeError:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Invalid session_info.json")
            return False
    
    def verify_security_code(self, temp_code):
        """
        Verify the temporary security code received via email
        
        Args:
            temp_code (str): The temporary security code from the verification email
            
        Returns:
            dict: Response data from the verification request
        """
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Verifying temporary security code...")
        
        if not self.session_info:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ No session information available")
            return None
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Please verify the security code using your browser:")
        print("")
        print("📱 BROWSER VERIFICATION REQUIRED")
        print("=" * 60)
        
        # Construct the verification URL with parameters
        verify_url = f"{PRIVACY_COM_URLS['code_verification']}?email={self.session_info['email']}&code={temp_code}&timestamp={datetime.now().isoformat()}"
        
        print(f"🌐 Open this URL in your browser:")
        print(f"   {verify_url}")
        print("")
        print("📋 Instructions:")
        print("1. Copy the URL above")
        print("2. Open it in your web browser (Chrome, Safari, Firefox, etc.)")
        print("3. Copy the entire JSON response from the browser")
        print("4. Paste it below")
        print("")
        
        if self.session_info["email"].endswith('@openai.com'):
            print("💡 OpenAI Employee with ChatGPT Agent:")
            print("If you're using a ChatGPT agent, ask it to:")
            print("- Open the URL in browser")
            print("- Copy the JSON response")
            print("- Provide the response back to you")
            print("")
        
        print("=" * 60)
        
        # Get the JSON response from user
        while True:
            print(f"Please paste the JSON response from: {verify_url}")
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
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Security code verified successfully!")
                    return response_data
                else:
                    error_msg = response_data.get("error", "Unknown error")
                    status_code = response_data.get("status_code", 0)
                    
                    if status_code == 400:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Invalid security code format")
                    elif status_code == 401:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Security code expired or invalid")
                    elif status_code == 429:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Rate limited. Please wait before trying again")
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Security code verification failed: {error_msg}")
                    
                    return None
                    
            except json.JSONDecodeError:
                print("❌ Invalid JSON response. Please make sure you copied the entire JSON response from the browser.")
                print("The response should look like: {\"success\": true, \"code\": \"...\", ...}")
                print("Please try again.")
                continue
    
    def complete_verification(self):
        """
        Complete the security verification process
        
        Returns:
            bool: True if verification was completed successfully
        """
        if not self.session_info:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ No session information available")
            return False
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Completing security verification...")
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Please complete security verification using your browser:")
        print("")
        print("📱 BROWSER VERIFICATION COMPLETION REQUIRED")
        print("=" * 60)
        
        # Construct the completion URL with parameters
        complete_url = f"{PRIVACY_COM_URLS['verification_complete']}?email={self.session_info['email']}&timestamp={datetime.now().isoformat()}"
        
        print(f"🌐 Open this URL in your browser:")
        print(f"   {complete_url}")
        print("")
        print("📋 Instructions:")
        print("1. Copy the URL above")
        print("2. Open it in your web browser")
        print("3. Copy the entire JSON response from the browser")
        print("4. Paste it below")
        print("")
        
        if self.session_info["email"].endswith('@openai.com'):
            print("💡 OpenAI Employee with ChatGPT Agent:")
            print("If you're using a ChatGPT agent, ask it to:")
            print("- Open the URL in browser")
            print("- Copy the JSON response")
            print("- Provide the response back to you")
            print("")
        
        print("=" * 60)
        
        # Get the JSON response from user
        while True:
            print(f"Please paste the JSON response from the verification completion request:")
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
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Security verification completed successfully!")
                    return True
                else:
                    error_msg = response_data.get("error", "Unknown error")
                    status_code = response_data.get("status_code", 0)
                    
                    if status_code == 400:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Invalid verification request")
                    elif status_code == 401:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Session expired. Please start over")
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Security verification failed: {error_msg}")
                    
                    return False
                    
            except json.JSONDecodeError:
                print("❌ Invalid JSON response. Please make sure you copied the entire JSON response from the browser.")
                print("The response should look like: {\"success\": true, \"message\": \"...\", ...}")
                print("Please try again.")
                continue


def main():
    if len(sys.argv) != 2:
        print("Usage: python security_code_verifier.py <temporary_security_code>")
        print("Example: python security_code_verifier.py ABC123")
        sys.exit(1)
    
    temp_code = sys.argv[1].strip()
    
    if not temp_code:
        print("❌ Please provide a temporary security code")
        sys.exit(1)
    
    print("=" * 60)
    print("Privacy.com Security Code Verifier")
    print("=" * 60)
    
    verifier = SecurityCodeVerifier()
    
    # Load session info from previous step
    if not verifier.load_session_info():
        sys.exit(1)
    
    # Verify the temporary security code
    verification_result = verifier.verify_security_code(temp_code)
    
    if not verification_result:
        print("\n❌ Security code verification failed. Please check your code and try again.")
        sys.exit(1)
    
    # Complete the security verification
    if verifier.complete_verification():
        print("\n" + "=" * 60)
        print("✅ SUCCESS!")
        print("Your Privacy.com security verification has been completed successfully.")
        print("You can now access the application.")
        print("=" * 60)
        
        # Clean up session file
        import os
        if os.path.exists("session_info.json"):
            os.remove("session_info.json")
            print("Session file cleaned up.")
    else:
        print("\n❌ Security verification completion failed. Please try again.")


if __name__ == "__main__":
    main() 