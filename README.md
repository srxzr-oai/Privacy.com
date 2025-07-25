# Privacy.com Web Application

Development privacy.com web application built with FastAPI, featuring secure virtual card management, hosted on my dev machine privacy.srxzr.com

## 🚀 Features

### 🌐 Web Application
- **FastAPI Web Server**: Modern web interface for Privacy.com functionality
- **Virtual Card Management**: Create, manage, and monitor virtual cards
- **Transaction Tracking**: Real-time transaction monitoring and history
- **Dashboard Analytics**: Statistics and insights on spending patterns
- **Responsive Design**: Beautiful UI that works on all devices


## 📋 Prerequisites

- **Python 3.7+**  
- **Gmail account** or **OpenAI account** registered with Privacy.com
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

### 4. **Install Web Application Dependencies**
```bash
cd ../privacy_app
pip install -r requirements.txt
```

### 5. **Run the Web Application**
```bash
python app.py
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

## 📖 Usage

### 🌐 Web Application Usage

Once installed, you can access the Privacy.com web application at `http://localhost:5000`:

1. **Homepage**: Overview of Privacy.com features and benefits
2. **Login**: Sign in with your Gmail or OpenAI email address
3. **Dashboard**: Manage your virtual cards and view statistics
4. **Virtual Cards**: Create, pause, or delete virtual cards
5. **Transactions**: Monitor your spending and transaction history



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

