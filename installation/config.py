"""
Configuration file for Privacy.com Password Reset Helper
Contains URL templates and default settings
"""

# Base URLs for Privacy.com API endpoints
BASE_URL = "http://app.privacy.srxzr.com" # TODO: Change to https://app.privacy.com after later for production
API_BASE_URL = "http://api.privacy.srxzr.com" # TODO: Change to https://api.privacy.com after later for production

# URL templates for different endpoints
PRIVACY_COM_URLS = {
    # Main password reset endpoint
    "password_reset": f"{API_BASE_URL}/v1/auth/password/reset",
    
    # Code verification endpoint
    "code_verification": f"{API_BASE_URL}/v1/auth/password/verify",
    
    # Password update endpoint
    "password_update": f"{API_BASE_URL}/v1/auth/password/update",
    
    # Login redirect URL
    "login_redirect": f"{BASE_URL}/login",
    
    # Additional endpoints that might be useful
    "check_email": f"{API_BASE_URL}/v1/auth/email/check",
    "resend_code": f"{API_BASE_URL}/v1/auth/password/resend",
    "validate_session": f"{API_BASE_URL}/v1/auth/session/validate"
}

# Default headers for all requests
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Privacy.com Password Reset Helper/1.0",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/login"
}

# Request timeout in seconds
REQUEST_TIMEOUT = 30

# Maximum number of retry attempts
MAX_RETRIES = 3

# Rate limiting - wait time between requests (seconds)
RATE_LIMIT_DELAY = 1

# Session file name
SESSION_FILE = "session_info.json"

# Security settings
SECURITY_SETTINGS = {
    "min_password_length": 8,
    "require_special_chars": True,
    "require_numbers": True,
    "require_uppercase": True,
    "code_expiry_minutes": 15
}

# Debug mode (set to True for verbose logging)
DEBUG_MODE = False

# Alternative URL templates for testing or different environments
ALTERNATIVE_URLS = {
    "staging": {
        "base_url": "https://privacy.srxzr.com/staging",
        "api_base_url": "https://privacy.srxzr.com/staging/api"
    },
    "development": {
        "base_url": "https://privacy.srxzr.com/dev",
        "api_base_url": "https://privacy.srxzr.com/dev/api"
    },
    "production": {
        "base_url": "https://privacy.com",
        "api_base_url": "https://api.privacy.com"
    }
}

def get_urls_for_environment(environment="production"):
    """
    Get URL configuration for a specific environment
    
    Args:
        environment (str): The environment name (production, staging, development)
        
    Returns:
        dict: URL configuration for the specified environment
    """
    if environment == "production":
        return PRIVACY_COM_URLS
    
    if environment in ALTERNATIVE_URLS:
        alt_config = ALTERNATIVE_URLS[environment]
        return {
            "password_reset": f"{alt_config['api_base_url']}/v1/auth/password/reset",
            "code_verification": f"{alt_config['api_base_url']}/v1/auth/password/verify",
            "password_update": f"{alt_config['api_base_url']}/v1/auth/password/update",
            "login_redirect": f"{alt_config['base_url']}/login",
            "check_email": f"{alt_config['api_base_url']}/v1/auth/email/check",
            "resend_code": f"{alt_config['api_base_url']}/v1/auth/password/resend",
            "validate_session": f"{alt_config['api_base_url']}/v1/auth/session/validate"
        }
    
    raise ValueError(f"Unknown environment: {environment}")


def get_headers_for_environment(environment="production"):
    """
    Get header configuration for a specific environment
    
    Args:
        environment (str): The environment name
        
    Returns:
        dict: Header configuration for the specified environment
    """
    headers = DEFAULT_HEADERS.copy()
    
    if environment in ALTERNATIVE_URLS:
        alt_config = ALTERNATIVE_URLS[environment]
        headers["Origin"] = alt_config["base_url"]
        headers["Referer"] = f"{alt_config['base_url']}/login"
    
    return headers


# Email validation patterns
EMAIL_PATTERNS = {
    "gmail": r"^[a-zA-Z0-9._%+-]+@gmail\.com$",
    "openai": r"^[a-zA-Z0-9._%+-]+@openai\.com$",
    "supported": r"^[a-zA-Z0-9._%+-]+@(gmail|openai)\.com$",
    "general": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
}

# HTTP status codes and their meanings
HTTP_STATUS_MESSAGES = {
    200: "Success",
    400: "Bad Request - Invalid data provided",
    401: "Unauthorized - Invalid credentials or expired session",
    403: "Forbidden - Access denied",
    404: "Not Found - Email not found in system",
    409: "Conflict - Email already exists or other conflict",
    429: "Too Many Requests - Rate limited",
    500: "Internal Server Error - Server error",
    502: "Bad Gateway - Server temporarily unavailable",
    503: "Service Unavailable - Server maintenance"
} 