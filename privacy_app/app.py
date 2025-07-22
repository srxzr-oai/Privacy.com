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


@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', user_email=session['user_email'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # TODO: Implement actual authentication
        # For now, simple validation
        if email and password:
            if email.endswith('@gmail.com') or email.endswith('@openai.com'):
                session['user_email'] = email
                session['login_time'] = datetime.now().isoformat()
                logger.info(f"User logged in: {email}")
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Please use a Gmail or OpenAI email address")
        else:
            return render_template('login.html', error="Please provide both email and password")
    
    return render_template('login.html')


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


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
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


if __name__ == '__main__':
    # Development server
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') == 'development'
    ) 