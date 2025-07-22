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
        
        try:
            verify_data = {
                "email": self.session_info["email"],
                "code": temp_code,
                "timestamp": datetime.now().isoformat()
            }
            
            response = self.session.post(
                PRIVACY_COM_URLS["code_verification"],
                json=verify_data,
                timeout=REQUEST_TIMEOUT
            )
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Code verified successfully!")
                return result
                
            elif response.status_code == 400:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Invalid code format")
                return None
                
            elif response.status_code == 401:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Code expired or invalid")
                return None
                
            elif response.status_code == 429:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Rate limited. Please wait before trying again")
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
        
        try:
            reset_data = {
                "email": self.session_info["email"],
                "new_password": new_password,
                "confirm_password": confirm_password,
                "timestamp": datetime.now().isoformat()
            }
            
            response = self.session.post(
                PRIVACY_COM_URLS["password_update"],
                json=reset_data,
                timeout=REQUEST_TIMEOUT
            )
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Response status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Password reset successfully!")
                return True
                
            elif response.status_code == 400:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Invalid password format")
                return False
                
            elif response.status_code == 401:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Session expired. Please start over")
                return False
                
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Unexpected response: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Request timed out")
            return False
            
        except requests.exceptions.ConnectionError:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Connection error")
            return False
            
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error: {str(e)}")
            return False


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