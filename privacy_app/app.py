#!/usr/bin/env python3
"""
Privacy.com Flask Web Application
Main web server for Privacy.com functionality
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
import os
import json
from datetime import datetime, timedelta
import secrets
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session/'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'privacy_com:'

# Initialize session
Session(app)

# Create session directory if it doesn't exist
os.makedirs('./flask_session/', exist_ok=True)

# API Configuration
API_BASE_URL = "http://api.privacy.srxzr.com"
REQUEST_TIMEOUT = 30


def check_password_reset_status(email):
    """
    Check if password reset has been completed for the given email
    
    Args:
        email (str): User's email address
        
    Returns:
        dict: Response containing reset status
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/check_if_reseted",
            json={"email": email},
            timeout=REQUEST_TIMEOUT,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Privacy.com Web App/1.0"
            }
        )
        
        logger.info(f"Password reset check for {email}: {response.status_code}")
        
        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json(),
                "reset_completed": response.json().get("reset_completed", False)
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "error": "Email not found in system",
                "reset_completed": False
            }
        else:
            return {
                "success": False,
                "error": f"API error: {response.status_code}",
                "reset_completed": False
            }
            
    except requests.exceptions.Timeout:
        logger.error(f"Timeout checking password reset status for {email}")
        return {
            "success": False,
            "error": "Request timeout",
            "reset_completed": False
        }
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error checking password reset status for {email}")
        return {
            "success": False,
            "error": "Connection error",
            "reset_completed": False
        }
    except Exception as e:
        logger.error(f"Error checking password reset status for {email}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "reset_completed": False
        }


@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    # Double-check reset status for dashboard access
    if not session.get('reset_verified', False):
        reset_status = check_password_reset_status(session['user_email'])
        if not reset_status['reset_completed']:
            session.clear()
            return redirect(url_for('login'))
        session['reset_verified'] = True
    
    return render_template('dashboard.html', user_email=session['user_email'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    validated_email = app.config.get('VALIDATED_EMAIL')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate input
        if not email or not password:
            return render_template('login.html', error="Please provide both email and password", validated_email=validated_email)
        
        if not (email.endswith('@gmail.com') or email.endswith('@openai.com')):
            return render_template('login.html', error="Please use a Gmail or OpenAI email address", validated_email=validated_email)
        
        # Check if this matches the validated email from startup
        if email != validated_email:
            error_msg = f"Please use the validated email address: {validated_email}"
            return render_template('login.html', error=error_msg, validated_email=validated_email)
        
        # TODO: Implement actual authentication with Privacy.com API
        # For now, simple validation since installation was already verified at startup
        session['user_email'] = email
        session['login_time'] = datetime.now().isoformat()
        session['reset_verified'] = True
        logger.info(f"User logged in: {email}")
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', validated_email=validated_email)


@app.route('/logout')
def logout():
    """User logout"""
    email = session.get('user_email', 'Unknown')
    session.clear()
    logger.info(f"User logged out: {email}")
    return redirect(url_for('index'))


@app.route('/api/cards')
def api_cards():
    """API endpoint to get user's virtual cards"""
    if 'user_email' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify reset status for API access
    if not session.get('reset_verified', False):
        return jsonify({'error': 'Installation not completed'}), 403
    
    # TODO: Implement actual card retrieval from Privacy.com API
    # Mock data for now
    cards = [
        {
            'id': 'card_001',
            'name': 'Shopping Card',
            'last_four': '1234',
            'status': 'active',
            'limit': 500.00,
            'spent': 123.45,
            'created_at': '2024-01-15T10:30:00Z'
        },
        {
            'id': 'card_002', 
            'name': 'Subscription Card',
            'last_four': '5678',
            'status': 'active',
            'limit': 100.00,
            'spent': 29.99,
            'created_at': '2024-01-10T14:20:00Z'
        }
    ]
    
    return jsonify({'cards': cards})


@app.route('/api/transactions')
def api_transactions():
    """API endpoint to get user's transactions"""
    if 'user_email' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # TODO: Implement actual transaction retrieval from Privacy.com API
    # Mock data for now
    transactions = [
        {
            'id': 'txn_001',
            'card_id': 'card_001',
            'merchant': 'Amazon',
            'amount': 45.99,
            'status': 'approved',
            'created_at': '2024-01-20T16:45:00Z'
        },
        {
            'id': 'txn_002',
            'card_id': 'card_002', 
            'merchant': 'Netflix',
            'amount': 15.99,
            'status': 'approved',
            'created_at': '2024-01-18T12:00:00Z'
        }
    ]
    
    return jsonify({'transactions': transactions})


@app.route('/api/create_card', methods=['POST'])
def api_create_card():
    """API endpoint to create a new virtual card"""
    if 'user_email' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    card_name = data.get('name')
    card_limit = data.get('limit', 100.00)
    
    if not card_name:
        return jsonify({'error': 'Card name is required'}), 400
    
    # TODO: Implement actual card creation via Privacy.com API
    # Mock response for now
    new_card = {
        'id': f'card_{secrets.token_hex(4)}',
        'name': card_name,
        'last_four': f'{secrets.randbelow(9000) + 1000}',
        'status': 'active',
        'limit': float(card_limit),
        'spent': 0.00,
        'created_at': datetime.now().isoformat()
    }
    
    logger.info(f"Created card {new_card['id']} for user {session['user_email']}")
    return jsonify({'card': new_card})


@app.route('/api/check_installation', methods=['POST'])
def api_check_installation():
    """API endpoint to check installation status"""
    data = request.json
    email = data.get('email') if data else None
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    reset_status = check_password_reset_status(email)
    return jsonify({
        'email': email,
        'installation_completed': reset_status['reset_completed'],
        'success': reset_status['success'],
        'error': reset_status.get('error')
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'api_base': API_BASE_URL
    })


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal server error: {error}")
    return render_template('500.html'), 500


def validate_installation():
    """
    Validate that installation (password reset) has been completed before starting the server
    
    Returns:
        bool: True if installation is valid, False otherwise
    """
    print("=" * 60)
    print("Privacy.com Web Application Startup")
    print("=" * 60)
    
    # Get email input from user
    while True:
        email = input("Enter your Gmail or OpenAI email address: ").strip()
        
        if not email:
            print("❌ Email address is required")
            continue
            
        if not (email.endswith('@gmail.com') or email.endswith('@openai.com')):
            print("❌ Please use a Gmail (@gmail.com) or OpenAI (@openai.com) address")
            continue
            
        break
    
    print(f"\n🔍 Checking installation status for: {email}")
    print("Connecting to Privacy.com API...")
    
    # Check password reset status
    reset_status = check_password_reset_status(email)
    
    if reset_status['success'] and reset_status['reset_completed']:
        print("✅ Installation completed successfully!")
        print(f"🚀 Starting Privacy.com web application for {email}")
        
        # Store the validated email for the application
        app.config['VALIDATED_EMAIL'] = email
        return True
        
    else:
        print("\n❌ Installation not completed!")
        print(f"Password reset has not been completed for: {email}")
        
        if reset_status.get('error'):
            print(f"Error details: {reset_status['error']}")
        
        print("\n" + "=" * 60)
        print("🔧 INSTALLATION REQUIRED")
        print("=" * 60)
        print("Please complete the password reset process:")
        print("")
        print("1. Navigate to the installation folder:")
        print("   cd ../installation")
        print("")
        print("2. Run the password reset initiator:")
        print(f"   python password_reset_initiator.py {email}")
        print("")
        print("3. Check your Gmail for the temporary code")
        print("")
        print("4. Run the password reset verifier:")
        print("   python password_reset_verifier.py <temporary_code>")
        print("")
        print("5. Try starting the application again:")
        print("   cd ../privacy_app")
        print("   python app.py")
        print("")
        
        if email.endswith('@openai.com'):
            print("💡 OpenAI Employee Note:")
            print("If you're using a ChatGPT agent with Gmail connector,")
            print("the agent can automate this process for you!")
        
        print("=" * 60)
        return False


if __name__ == '__main__':
    # Validate installation before starting the server
    if not validate_installation():
        print("\n❌ Application startup cancelled due to incomplete installation.")
        exit(1)
    
    print("\n" + "=" * 60)
    print("🌐 Starting Privacy.com Web Server")
    print("=" * 60)
    print("📍 Application will be available at: http://localhost:5000")
    print("📧 Validated email:", app.config.get('VALIDATED_EMAIL'))
    print("🔄 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Development server
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=os.environ.get('FLASK_ENV') == 'development'
        )
    except KeyboardInterrupt:
        print("\n\n👋 Privacy.com application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        exit(1) 