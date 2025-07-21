# Privacy.com Password Reset Helper

A Python utility to help automate the password reset process for Privacy.com accounts. This tool consists of two scripts that work together to initiate and complete the password reset flow.

## 🚀 Features

- **Two-step password reset process**: Initiate reset and verify with temporary code
- **Gmail integration**: Specifically designed for Gmail accounts
- **Session management**: Maintains session state between steps
- **Error handling**: Comprehensive error messages and status reporting
- **Rate limiting protection**: Built-in delays to avoid API rate limits
- **Secure password handling**: Uses getpass for secure password input
- **Environment support**: Configurable for different environments (production, staging, development)

## 📋 Prerequisites

- **Python 3.7+** 
- **Gmail account** registered with Privacy.com
- **Internet connection**

## 🛠 Installation

1. **Clone or download this repository**:
   ```bash
   git clone <repository-url>
   cd privacy-com-password-reset
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python --version  # Should show Python 3.7+
   pip list | grep requests  # Should show requests package
   ```

## 📖 Usage

### Step 1: Initiate Password Reset

Run the first script with your Gmail address:

```bash
python password_reset_initiator.py your.email@gmail.com
```

**Example**:
```bash
python password_reset_initiator.py john.doe@gmail.com
```

**What this script does**:
- ✅ Validates your Gmail address format
- 🌐 Sends a password reset request to Privacy.com
- 💾 Saves session information for the next step
- 📧 Tells you to check your email for the reset code

**Expected output**:
```
============================================================
Privacy.com Password Reset Initiator
============================================================
[14:30:15] Initiating password reset for: john.doe@gmail.com
[14:30:15] Sending reset request to Privacy.com...
[14:30:16] Response status: 200
[14:30:16] ✅ Password reset initiated successfully!
[14:30:16] Check your email for reset instructions
[14:30:16] Session info saved to session_info.json

============================================================
✅ NEXT STEPS:
1. Check your Gmail inbox for the reset email
2. Look for the temporary reset code in the email
3. Run: python password_reset_verifier.py <temporary_code>
============================================================
```

### Step 2: Verify Code and Reset Password

After receiving the temporary code in your email, run the second script:

```bash
python password_reset_verifier.py <temporary_code>
```

**Example**:
```bash
python password_reset_verifier.py ABC123
```

**What this script does**:
- 🔍 Loads session information from step 1
- ✅ Verifies the temporary code with Privacy.com
- 🔐 Prompts you to enter a new password (securely)
- 🔄 Updates your password
- 🧹 Cleans up temporary session files

**Expected output**:
```
============================================================
Privacy.com Password Reset Verifier
============================================================
[14:35:20] Session info loaded for: john.doe@gmail.com
[14:35:20] Verifying temporary code...
[14:35:21] Response status: 200
[14:35:21] ✅ Code verified successfully!

============================================================
Enter your new password:
New password: ••••••••
Confirm password: ••••••••
[14:35:30] Resetting password...
[14:35:31] Response status: 200
[14:35:31] ✅ Password reset successfully!

============================================================
✅ SUCCESS!
Your Privacy.com password has been reset successfully.
You can now login with your new password.
============================================================
Session file cleaned up.
```

## 🔧 Configuration

### URL Templates

The `config.py` file contains all URL templates and settings:

```python
PRIVACY_COM_URLS = {
    "password_reset": "https://api.privacy.com/v1/auth/password/reset",
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
        "base_url": "https://staging.privacy.com",
        "api_base_url": "https://staging-api.privacy.com"
    }
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
| `❌ Please provide a Gmail address` | Non-Gmail email provided | Use a Gmail address |
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

## 📁 File Structure

```
privacy-com-password-reset/
├── password_reset_initiator.py    # Step 1: Initiate reset
├── password_reset_verifier.py     # Step 2: Verify code & reset
├── config.py                      # URL templates & settings
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── session_info.json             # Temporary session data (auto-generated)
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

- **Gmail Only**: Currently supports Gmail addresses only
- **Single Session**: One password reset at a time
- **Time Sensitive**: Temporary codes expire (usually 15 minutes)
- **Rate Limited**: Respect Privacy.com's rate limits

## 🤝 Support

If you encounter issues:

1. **Check the error message** - Most issues have clear error descriptions
2. **Verify prerequisites** - Ensure Python 3.7+ and dependencies are installed
3. **Check network** - Ensure stable internet connection
4. **Review logs** - Check the timestamp messages for clues

## 📄 License

This tool is provided as-is for educational and personal use. Please respect Privacy.com's terms of service and API usage policies.

## ⚠️ Disclaimer

This is an unofficial tool and is not affiliated with or endorsed by Privacy.com. Use at your own risk and ensure compliance with Privacy.com's terms of service.
