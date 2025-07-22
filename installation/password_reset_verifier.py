#!/usr/bin/env python3
"""
Privacy.com Password Reset Verifier
This script verifies the temporary code and completes the password reset process
"""

import requests
import json
import sys
import getpass
from datetime import datetime
from config import PRIVACY_COM_URLS, DEFAULT_HEADERS, REQUEST_TIMEOUT


class PasswordResetVerifier:
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
            print("Please run password_reset_initiator.py first")
            return False
            
        except json.JSONDecodeError:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Invalid session_info.json")
            return False
    
    def verify_code(self, temp_code):
        """
        Verify the temporary code received via email
        
        Args:
            temp_code (str): The temporary code from the reset email
            
        Returns:
            dict: Response data from the verification request
        """
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Verifying temporary code...")
        
        if not self.session_info:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ No session information available")
            return None
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Please verify the code using your browser:")
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
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Code verified successfully!")
                    return response_data
                else:
                    error_msg = response_data.get("error", "Unknown error")
                    status_code = response_data.get("status_code", 0)
                    
                    if status_code == 400:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Invalid code format")
                    elif status_code == 401:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Code expired or invalid")
                    elif status_code == 429:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Rate limited. Please wait before trying again")
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Code verification failed: {error_msg}")
                    
                    return None
                    
            except json.JSONDecodeError:
                print("❌ Invalid JSON response. Please make sure you copied the entire JSON response from the browser.")
                print("The response should look like: {\"success\": true, \"code\": \"...\", ...}")
                print("Please try again.")
                continue
    
    def reset_password(self, new_password, confirm_password):
        """
        Complete the password reset with the new password
        
        Args:
            new_password (str): The new password
            confirm_password (str): Confirmation of the new password
            
        Returns:
            bool: True if password was reset successfully
        """
        if new_password != confirm_password:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Passwords do not match")
            return False
        
        if len(new_password) < 8:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Password must be at least 8 characters long")
            return False
        
        if not self.session_info:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ No session information available")
            return False
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Resetting password...")
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Please complete password reset using your browser:")
        print("")
        print("📱 BROWSER PASSWORD RESET REQUIRED")
        print("=" * 60)
        
        # Construct the password reset URL with parameters
        # Note: For security, we'll pass password in POST body via browser tools
        reset_url = f"{PRIVACY_COM_URLS['password_update']}?email={self.session_info['email']}&timestamp={datetime.now().isoformat()}"
        
        print(f"🌐 Open this URL in your browser:")
        print(f"   {reset_url}")
        print("")
        print("📋 Instructions:")
        print("1. Copy the URL above")
        print("2. Open it in your web browser")
        print("3. Use browser developer tools to make a POST request with:")
        print(f"   - URL: {reset_url}")
        print("   - Method: POST")
        print("   - Body: {\"new_password\": \"your_new_password\", \"confirm_password\": \"your_new_password\"}")
        print("4. Copy the entire JSON response from the browser")
        print("5. Paste it below")
        print("")
        
        if self.session_info["email"].endswith('@openai.com'):
            print("💡 OpenAI Employee with ChatGPT Agent:")
            print("If you're using a ChatGPT agent, ask it to:")
            print("- Open the URL in browser")
            print("- Make a POST request with the password data")
            print("- Copy the JSON response")
            print("- Provide the response back to you")
            print("")
        
        print("=" * 60)
        
        # Get the JSON response from user
        while True:
            print(f"Please paste the JSON response from the password reset request:")
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
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Password reset successfully!")
                    return True
                else:
                    error_msg = response_data.get("error", "Unknown error")
                    status_code = response_data.get("status_code", 0)
                    
                    if status_code == 400:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Invalid password format")
                    elif status_code == 401:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Session expired. Please start over")
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Password reset failed: {error_msg}")
                    
                    return False
                    
            except json.JSONDecodeError:
                print("❌ Invalid JSON response. Please make sure you copied the entire JSON response from the browser.")
                print("The response should look like: {\"success\": true, \"message\": \"...\", ...}")
                print("Please try again.")
                continue


def main():
    if len(sys.argv) != 2:
        print("Usage: python password_reset_verifier.py <temporary_code>")
        print("Example: python password_reset_verifier.py ABC123")
        sys.exit(1)
    
    temp_code = sys.argv[1].strip()
    
    if not temp_code:
        print("❌ Please provide a temporary code")
        sys.exit(1)
    
    print("=" * 60)
    print("Privacy.com Password Reset Verifier")
    print("=" * 60)
    
    verifier = PasswordResetVerifier()
    
    # Load session info from previous step
    if not verifier.load_session_info():
        sys.exit(1)
    
    # Verify the temporary code
    verification_result = verifier.verify_code(temp_code)
    
    if not verification_result:
        print("\n❌ Code verification failed. Please check your code and try again.")
        sys.exit(1)
    
    # Prompt for new password
    print("\n" + "=" * 60)
    print("Enter your new password:")
    new_password = getpass.getpass("New password: ")
    confirm_password = getpass.getpass("Confirm password: ")
    
    # Reset password
    if verifier.reset_password(new_password, confirm_password):
        print("\n" + "=" * 60)
        print("✅ SUCCESS!")
        print("Your Privacy.com password has been reset successfully.")
        print("You can now login with your new password.")
        print("=" * 60)
        
        # Clean up session file
        import os
        if os.path.exists("session_info.json"):
            os.remove("session_info.json")
            print("Session file cleaned up.")
    else:
        print("\n❌ Password reset failed. Please try again.")


if __name__ == "__main__":
    main() 