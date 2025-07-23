#!/usr/bin/env python3
"""
Simple FastAPI server runner
Run this instead of using fastapi[standard] command
"""

import os
import sys
import traceback

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import fastapi
        print("✅ FastAPI found")
    except ImportError:
        missing_deps.append("fastapi")
    
    try:
        import uvicorn
        print("✅ Uvicorn found")
    except ImportError:
        missing_deps.append("uvicorn")
    
    try:
        import jinja2
        print("✅ Jinja2 found")
    except ImportError:
        missing_deps.append("jinja2")
    
    if missing_deps:
        print("\n❌ Missing dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nInstall with:")
        print(f"   pip install {' '.join(missing_deps)}")
        return False
    
    return True

def main():
    print("Privacy.com FastAPI Server")
    print("=" * 50)
    
    # Check dependencies first
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("\n🔍 Testing application import...")
    try:
        from app import app
        print("✅ Application imported successfully")
    except Exception as e:
        print(f"❌ Error importing application: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)
    
    print("\n🚀 Starting server with uvicorn...")
    print("📍 Server will be available at: http://localhost:8000")
    print("🔄 Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        import uvicorn
        
        # Run the server using import string for proper reload
        uvicorn.run(
            "app:app",  # Use import string instead of app object
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=["."],
            reload_excludes=["__pycache__", "*.pyc"],
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 