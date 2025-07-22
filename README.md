# Privacy.com Web Application

A comprehensive Privacy.com web application built with Flask, featuring secure virtual card management and an automated security verification system for account setup.

## 🚀 Features

### 🌐 Web Application
- **FastAPI Web Server**: Modern web interface for Privacy.com functionality
- **Virtual Card Management**: Create, manage, and monitor virtual cards
- **Transaction Tracking**: Real-time transaction monitoring and history
- **Dashboard Analytics**: Statistics and insights on spending patterns
- **Responsive Design**: Beautiful UI that works on all devices


## 📋 Prerequisites

- **Python 3.7+** 
- **Gmail account** registered with Privacy.com
- **Internet connection**

## 🛠 Installation

### 1. **Clone the Repository**
```bash
git clone <repository-url>
cd Privacy.com
```

### 2. **Install Installation Dependencies**
```bash
cd installation
pip install -r requirements.txt
```

### 3. **🔐 Setup Security Verification (Required)**
Before running the main application, you need to complete Privacy.com security verification:

#### For Regular Users:
```bash
# Step 1: Initiate security verification
python security_code_initiator.py your.email@gmail.com

# Step 2: Check your Gmail for the temporary security code, then run:
python security_code_verifier.py <temporary_code>
```

### 4. **Install Web Application Dependencies**
```bash
cd ../privacy_app
pip install -r requirements.txt
```

### 5. **Run the Web Application**
```bash
python app.py
```

**Or using uvicorn directly (also includes validation):**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

**Both methods will prompt you for your email address and verify installation before starting:**

```
============================================================
Privacy.com Web Application Startup
============================================================
Enter your Gmail or OpenAI email address: user@gmail.com

🔍 Checking installation status for: user@gmail.com
Connecting to Privacy.com API...
✅ Installation completed successfully!
🚀 Starting Privacy.com web application for user@gmail.com

============================================================
🌐 Starting Privacy.com Web Server
============================================================
📍 Application will be available at: http://localhost:8000
📧 Validated email: user@gmail.com
🔄 Press Ctrl+C to stop the server
============================================================
```

**If installation is not completed, you'll see:**
```
❌ Installation not completed!
Security verification has not been completed for: user@gmail.com

============================================================
🔧 INSTALLATION REQUIRED
============================================================
Please complete the security verification process:

1. Navigate to the installation folder:
   cd ../installation

2. Run the security code initiator:
   python security_code_initiator.py user@gmail.com

3. Check your Gmail for the temporary security code

4. Run the security code verifier:
   python security_code_verifier.py <temporary_code>

5. Try starting the application again:
   cd ../privacy_app
   python app.py
============================================================
```

## 📖 Usage

### 🌐 Web Application Usage

Once installed, you can access the Privacy.com web application at `http://localhost:5000`:

1. **Homepage**: Overview of Privacy.com features and benefits
2. **Login**: Sign in with your Gmail or OpenAI email address
3. **Dashboard**: Manage your virtual cards and view statistics
4. **Virtual Cards**: Create, pause, or delete virtual cards
5. **Transactions**: Monitor your spending and transaction history


## 🔧 Configuration

### URL Templates

The `config.py` file contains all URL templates and settings:

```python
PRIVACY_COM_URLS = {
    "password_reset": "https://api.privacy.com/v1/auth/password/reset", # NOTE: these are prod ones and do not work in dev mode
    "code_verification": "https://api.privacy.com/v1/auth/password/verify",
    "password_update": "https://api.privacy.com/v1/auth/password/update",
    # ... more URLs
}
```

### Environment Configuration

You can configure different environments by modifying `config.py`:

```python
# For staging environment
ALTERNATIVE_URLS = {
    "staging": {
        "base_url": "https://privacy.srxzr.com/staging",
        "api_base_url": "https://privacy.srxzr.com/staging/api"
    },
    "development": {
        "base_url": "https://privacy.srxzr.com/dev",
        "api_base_url": "https://privacy.srxzr.com/dev/api"
    },
}
```

### Request Settings

Customize timeouts and retry settings:

```python
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 1  # seconds between requests
```

## ❌ Error Handling

### Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| `❌ Please provide a Gmail (@gmail.com) or OpenAI (@openai.com) address` | Unsupported email domain | Use a Gmail or OpenAI address |
| `❌ Email not found in Privacy.com system` | Email not registered | Register the email with Privacy.com first |
| `⚠️ Rate limited` | Too many requests | Wait a few minutes and try again |
| `❌ Code expired or invalid` | Temporary code is wrong/expired | Check your email for the correct code |
| `❌ session_info.json not found` | Step 2 run before Step 1 | Run the initiator script first |
| `❌ Connection error` | Network issues | Check your internet connection |

### HTTP Status Codes

- **200**: Success
- **400**: Bad Request - Invalid data
- **401**: Unauthorized - Invalid/expired session
- **404**: Not Found - Email not in system
- **429**: Rate Limited - Too many requests
- **500**: Server Error - Privacy.com server issue

## 📁 Project Structure

```
Privacy.com/
├── installation/                   # Security verification installation system
│   ├── security_code_initiator.py    # Step 1: Initiate verification
│   ├── security_code_verifier.py     # Step 2: Verify security code
│   ├── config.py                      # URL templates & settings
│   ├── utils.py                       # Utility functions
│   ├── requirements.txt               # Installation dependencies
│   └── session_info.json             # Temporary session data (auto-generated)
├── privacy_app/                    # Main FastAPI web application
│   ├── app.py                         # FastAPI application entry point
│   ├── requirements.txt               # Web app dependencies
│   ├── templates/                     # HTML templates
│   │   ├── base.html                  # Base template
│   │   ├── index.html                 # Homepage
│   │   ├── login.html                 # Login page
│   │   └── dashboard.html             # User dashboard
│   └── static/                        # Static assets
│       ├── css/style.css              # Custom styles
│       └── js/app.js                  # JavaScript functionality
└── README.md                       # This file
```

## 🔒 Security Notes

1. **Session File**: The `session_info.json` file contains temporary session data. It's automatically deleted after successful password reset.

2. **Password Input**: Passwords are entered securely using Python's `getpass` module (not visible on screen).

3. **HTTPS Only**: All communication uses HTTPS encryption.

4. **No Password Storage**: This tool never stores your passwords.

## 🔄 Troubleshooting

### Script Won't Start
```bash
# Check Python version
python --version

# Install dependencies
pip install -r requirements.txt

# Check file permissions
ls -la *.py
```

### Can't Receive Email
- Check spam/junk folder
- Ensure email is registered with Privacy.com
- Wait a few minutes for email delivery
- Try initiating reset again

### Code Verification Fails
- Double-check the code from your email
- Ensure code hasn't expired (usually 15 minutes)
- Make sure you ran the initiator script first
- Check that `session_info.json` exists

### Password Reset Fails
- Ensure passwords match
- Use a strong password (8+ characters)
- Check internet connection
- Verify session hasn't expired

## 🛡 Limitations

- **Supported Email Domains**: Currently supports Gmail (@gmail.com) and OpenAI (@openai.com) addresses only
- **Single Session**: One security verification at a time
- **Time Sensitive**: Temporary security codes expire (usually 15 minutes)
- **Rate Limited**: Respect Privacy.com's rate limits

## 🤝 Support

If you encounter issues:

1. **Check the error message** - Most issues have clear error descriptions
2. **Verify prerequisites** - Ensure Python 3.7+ and dependencies are installed
3. **Check network** - Ensure stable internet connection
4. **Review logs** - Check the timestamp messages for clues

**Workflow**:
1. Provide step-by-step instructions
2. Guide user through manual email entry and code retrieval
3. Assist with troubleshooting as needed -->

## 📄 License

This tool is provided as-is for educational and personal use. Please respect Privacy.com's terms of service and API usage policies.

