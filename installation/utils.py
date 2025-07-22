"""
Utility functions for Privacy.com Security Verification Helper
Contains validation, logging, and helper functions
"""

import re
import json
import os
from datetime import datetime, timedelta
from config import EMAIL_PATTERNS, SECURITY_SETTINGS, SESSION_FILE


def validate_email(email, supported_only=True):
    """
    Validate email address format
    
    Args:
        email (str): Email address to validate
        supported_only (bool): If True, only accept Gmail and OpenAI addresses
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "Email address is required"
    
    email = email.strip().lower()
    
    if not email:
        return False, "Email address cannot be empty"
    
    if supported_only:
        pattern = EMAIL_PATTERNS["supported"]
        if not re.match(pattern, email):
            return False, "Please provide a valid Gmail (@gmail.com) or OpenAI (@openai.com) address"
    else:
        pattern = EMAIL_PATTERNS["general"]
        if not re.match(pattern, email):
            return False, "Please provide a valid email address"
    
    return True, None


def validate_security_code(code):
    """
    Validate security code format based on security settings
    
    Args:
        code (str): Security code to validate
        
    Returns:
        tuple: (is_valid, error_messages_list)
    """
    if not code:
        return False, ["Security code is required"]
    
    errors = []
    settings = SECURITY_SETTINGS
    
    # Check minimum length
    if len(code) < settings["min_code_length"]:
        errors.append(f"Security code must be at least {settings['min_code_length']} characters long")
    
    # Check maximum length
    if len(code) > settings["max_code_length"]:
        errors.append(f"Security code must be no more than {settings['max_code_length']} characters long")
    
    # Check for valid characters (alphanumeric only)
    if not re.match(r'^[A-Za-z0-9]+$', code):
        errors.append("Security code must contain only letters and numbers")
    
    return len(errors) == 0, errors


def validate_temporary_security_code(code):
    """
    Validate temporary security code format
    
    Args:
        code (str): Temporary security code to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not code or not isinstance(code, str):
        return False, "Temporary security code is required"
    
    code = code.strip().upper()
    
    if not code:
        return False, "Temporary security code cannot be empty"
    
    # Basic format validation (alphanumeric, 4-10 characters)
    if not re.match(r'^[A-Z0-9]{4,10}$', code):
        return False, "Temporary security code must be 4-10 alphanumeric characters"
    
    return True, None


def log_message(message, level="INFO"):
    """
    Log a message with timestamp
    
    Args:
        message (str): Message to log
        level (str): Log level (INFO, WARNING, ERROR)
    """
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {level}: {message}")


def save_session_data(email, response_data, cookies=None):
    """
    Save session data to file
    
    Args:
        email (str): User email
        response_data (dict): Response data from API
        cookies (dict): Session cookies
        
    Returns:
        bool: True if saved successfully
    """
    try:
        session_info = {
            "email": email,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data,
            "cookies": cookies or {},
            "expires_at": (datetime.now() + timedelta(minutes=SECURITY_SETTINGS["code_expiry_minutes"])).isoformat()
        }
        
        with open(SESSION_FILE, "w") as f:
            json.dump(session_info, f, indent=2)
        
        return True
        
    except Exception as e:
        log_message(f"Failed to save session data: {str(e)}", "ERROR")
        return False


def load_session_data():
    """
    Load session data from file
    
    Returns:
        dict or None: Session data if valid, None otherwise
    """
    try:
        if not os.path.exists(SESSION_FILE):
            log_message("Session file not found", "ERROR")
            return None
        
        with open(SESSION_FILE, "r") as f:
            session_info = json.load(f)
        
        # Check if session has expired
        expires_at = datetime.fromisoformat(session_info.get("expires_at", ""))
        if datetime.now() > expires_at:
            log_message("Session has expired", "ERROR")
            cleanup_session_file()
            return None
        
        return session_info
        
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        log_message(f"Failed to load session data: {str(e)}", "ERROR")
        return None


def cleanup_session_file():
    """
    Remove session file if it exists
    
    Returns:
        bool: True if cleaned up successfully
    """
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
            log_message("Session file cleaned up")
            return True
        return True
        
    except Exception as e:
        log_message(f"Failed to cleanup session file: {str(e)}", "ERROR")
        return False


def format_error_response(status_code, response_text=""):
    """
    Format error response based on HTTP status code
    
    Args:
        status_code (int): HTTP status code
        response_text (str): Response text from server
        
    Returns:
        str: Formatted error message
    """
    from config import HTTP_STATUS_MESSAGES
    
    base_message = HTTP_STATUS_MESSAGES.get(status_code, f"Unknown error (HTTP {status_code})")
    
    if response_text and len(response_text) < 200:
        return f"{base_message}\nServer response: {response_text}"
    
    return base_message


def print_banner(title):
    """
    Print a formatted banner
    
    Args:
        title (str): Title to display in banner
    """
    border = "=" * 60
    print(border)
    print(title.center(60))
    print(border)


def print_success_message(message):
    """
    Print a success message with formatting
    
    Args:
        message (str): Success message to display
    """
    print(f"\n{'=' * 60}")
    print("✅ SUCCESS!")
    print(message)
    print("=" * 60)


def print_error_message(message):
    """
    Print an error message with formatting
    
    Args:
        message (str): Error message to display
    """
    print(f"\n❌ ERROR: {message}")


def print_next_steps(steps_list):
    """
    Print next steps with formatting
    
    Args:
        steps_list (list): List of steps to display
    """
    print(f"\n{'=' * 60}")
    print("✅ NEXT STEPS:")
    for i, step in enumerate(steps_list, 1):
        print(f"{i}. {step}")
    print("=" * 60)


def get_user_input(prompt, hidden=False):
    """
    Get user input with optional hidden input for sensitive data
    
    Args:
        prompt (str): Input prompt
        hidden (bool): If True, hide input (for sensitive data)
        
    Returns:
        str: User input
    """
    if hidden:
        import getpass
        return getpass.getpass(prompt)
    else:
        return input(prompt).strip()


def retry_on_failure(func, max_retries=3, delay=1):
    """
    Retry a function on failure
    
    Args:
        func (callable): Function to retry
        max_retries (int): Maximum number of retries
        delay (int): Delay between retries in seconds
        
    Returns:
        Result of function call or None if all retries failed
    """
    import time
    
    for attempt in range(max_retries):
        try:
            result = func()
            if result is not None:
                return result
        except Exception as e:
            log_message(f"Attempt {attempt + 1} failed: {str(e)}", "WARNING")
        
        if attempt < max_retries - 1:
            log_message(f"Retrying in {delay} seconds...", "INFO")
            time.sleep(delay)
    
    log_message(f"All {max_retries} attempts failed", "ERROR")
    return None 