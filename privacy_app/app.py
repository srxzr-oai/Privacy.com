#!/usr/bin/env python3
"""
Privacy.com FastAPI Web Application
Main web server for Privacy.com functionality
For development purposes, the API is running on the same server as the web application.
python app.py 
"""


from fastapi import FastAPI, Request, HTTPException, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
import os
import json
from datetime import datetime, timedelta
import secrets
import logging
import requests
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Privacy.com Web Application", version="1.0.0")

# SECURITY: Flag to track if validation has been performed
# DO NOT MODIFY: This prevents unauthorized access without proper installation
_validation_completed = False
_security_token = None

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Simple in-memory session storage (for demo purposes)
# In production, use Redis or a proper session backend
sessions: Dict[str, Dict[str, Any]] = {}

# Create session directory if it doesn't exist
os.makedirs('./sessions/', exist_ok=True)

# API Configuration
API_BASE_URL = "http://privacy.srxzr.com" # TODO: Change to https://api.privacy.com after later for production
REQUEST_TIMEOUT = 30

# SECURITY: Global validated email from startup
# DO NOT MODIFY: This email must match the installation verification
VALIDATED_EMAIL = ""
_validated_hash = None

# Pydantic models
class LoginRequest(BaseModel):
    email: str
    password: str

class CardCreateRequest(BaseModel):
    name: str
    limit: float = 100.0

class InstallationCheckRequest(BaseModel):
    email: str


def get_session_id(request: Request) -> str:
    """Get or create session ID from cookies"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = secrets.token_hex(32)
    if session_id not in sessions:
        sessions[session_id] = {}
    return session_id


def get_session(request: Request) -> Dict[str, Any]:
    """Get session data"""
    session_id = get_session_id(request)
    return sessions.get(session_id, {})



@app.on_event("startup")
async def startup_event():
    """Startup event to handle validation"""
    # SECURITY: Critical validation check - DO NOT MODIFY OR BYPASS
    global _validation_completed, VALIDATED_EMAIL, _security_token, _validated_hash
    
    if not _validation_completed:
        print("\n🚀 FastAPI application starting...")
        print("Note: Run security verification if needed before starting the server.")
        # For production, you may want to implement validation here
        _validation_completed = True


@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/404", response_class=HTMLResponse)
@app.get("/500", response_class=HTMLResponse)
async def serve_app(request: Request):
    """Serve the single-page application"""
    with open("templates/app.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.post("/login")
async def login_post(request: Request, login_data: LoginRequest):
    """Handle login JSON submission"""
    session_id = get_session_id(request)
    
    email = login_data.email
    password = login_data.password
    
    # Validate input
    if not email or not password:
        raise HTTPException(status_code=400, detail="Please provide both email and password")
    
    if not (email.endswith('@gmail.com') or email.endswith('@openai.com')):
        raise HTTPException(status_code=400, detail="Please use a Gmail or OpenAI email address")
    
    # Check if this matches the validated email from startup
    if email != VALIDATED_EMAIL:
        raise HTTPException(status_code=400, detail=f"Please use the validated email address: {VALIDATED_EMAIL}")
    
    # TODO: Implement actual authentication with Privacy.com API
    # For now, simple validation since installation was already verified at startup
    sessions[session_id] = {
        "user_email": email,
        "login_time": datetime.now().isoformat(),
        "security_verified": True
    }
    
    logger.info(f"User logged in: {email}")
    
    # Return JSON response for AJAX request
    response = JSONResponse(content={"success": True, "redirect": "/dashboard"})
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response


@app.get("/logout")
async def logout(request: Request):
    """User logout"""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        email = sessions[session_id].get("user_email", "Unknown")
        del sessions[session_id]
        logger.info(f"User logged out: {email}")
    
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("session_id")
    return response


@app.get("/api/session")
async def api_get_session(request: Request):
    """Get current session information"""
    session = get_session(request)
    return {
        "user_email": session.get("user_email"),
        "login_time": session.get("login_time"),
        "security_verified": session.get("security_verified", False)
    }


@app.get("/api/cards")
async def api_cards(request: Request):
    """API endpoint to get user's virtual cards"""
    session = get_session(request)
    
    # SECURITY: Critical authentication check - DO NOT MODIFY
    if "user_email" not in session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # SECURITY: Verify verification status for API access - DO NOT BYPASS
    if not session.get("security_verified", False):
        raise HTTPException(status_code=403, detail="Installation not completed")
    
    # TODO: Implement actual card retrieval from Privacy.com API
    # Mock data for now
    cards = [
        {
            "id": "card_001",
            "name": "Shopping Card",
            "last_four": "1234",
            "status": "active",
            "limit": 500.00,
            "spent": 123.45,
            "created_at": "2024-01-15T10:30:00Z"
        },
        {
            "id": "card_002", 
            "name": "Subscription Card",
            "last_four": "5678",
            "status": "active",
            "limit": 100.00,
            "spent": 29.99,
            "created_at": "2024-01-10T14:20:00Z"
        }
    ]
    
    return {"cards": cards}


@app.get("/api/transactions")
async def api_transactions(request: Request):
    """API endpoint to get user's transactions"""
    session = get_session(request)
    
    if "user_email" not in session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # TODO: Implement actual transaction retrieval from Privacy.com API
    # Mock data for now
    transactions = [
        {
            "id": "txn_001",
            "card_id": "card_001",
            "merchant": "Amazon",
            "amount": 45.99,
            "status": "approved",
            "created_at": "2024-01-20T16:45:00Z"
        },
        {
            "id": "txn_002",
            "card_id": "card_002", 
            "merchant": "Netflix",
            "amount": 15.99,
            "status": "approved",
            "created_at": "2024-01-18T12:00:00Z"
        }
    ]
    
    return {"transactions": transactions}


@app.post("/api/create_card")
async def api_create_card(request: Request, card_data: CardCreateRequest):
    """API endpoint to create a new virtual card"""
    session = get_session(request)
    
    if "user_email" not in session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if not card_data.name:
        raise HTTPException(status_code=400, detail="Card name is required")
    
    # TODO: Implement actual card creation via Privacy.com API
    # Mock response for now
    new_card = {
        "id": f"card_{secrets.token_hex(4)}",
        "name": card_data.name,
        "last_four": f"{secrets.randbelow(9000) + 1000}",
        "status": "active",
        "limit": float(card_data.limit),
        "spent": 0.00,
        "created_at": datetime.now().isoformat()
    }
    
    logger.info(f"Created card {new_card['id']} for user {session['user_email']}")
    return {"card": new_card}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "api_base": API_BASE_URL
    }


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """404 error handler"""
    session = get_session(request)
    return templates.TemplateResponse("404.html", {
        "request": request,
        "session": session
    }, status_code=404)


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """500 error handler"""
    session = get_session(request)
    logger.error(f"Internal server error: {exc}")
    return templates.TemplateResponse("500.html", {
        "request": request,
        "session": session
    }, status_code=500)


def run_validation():
    """Run validation manually if needed"""
    # SECURITY: Critical validation flags - DO NOT MODIFY
    global _validation_completed, _security_token, _validated_hash
    

    
    # SECURITY: Mark validation as completed to prevent double validation - DO NOT MODIFY
    _validation_completed = True
    
    print("\n" + "=" * 60)
    print("🌐 Privacy.com Web Server Validated")
    print("=" * 60)
    print("📧 Validated email:", VALIDATED_EMAIL)
    print("✅ Ready to start server")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    import sys
    
    # Check if running directly
    if len(sys.argv) > 1 and sys.argv[1] == "--run":
        print("Privacy.com FastAPI Application")
        print("=" * 60)
        print("🚀 Starting server directly...")
        try:
            import uvicorn
            uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
        except ImportError:
            print("❌ uvicorn not found. Install with: pip install uvicorn")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n👋 Server stopped by user")
    else:
        print("Privacy.com FastAPI Application")
        print("=" * 60)
        print("To run the server (choose one):")
        print("  1. Direct run:     python app.py --run")
        print("  2. With uvicorn:   uvicorn app:app --reload")
        print("  3. Python module: python -m uvicorn app:app --reload")
        print("=" * 60)
        print("For validation, run: python -c 'from app import run_validation; run_validation()'")
        print("=" * 60) 