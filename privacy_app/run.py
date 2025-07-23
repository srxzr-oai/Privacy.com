#!/usr/bin/env python3
"""
Simple FastAPI server runner
Run this instead of using fastapi[standard] command
"""

import os
import sys

def main():
    print("Privacy.com FastAPI Server")
    print("=" * 50)
    
    try:
        import uvicorn
        print("🚀 Starting server with uvicorn...")
        print("📍 Server will be available at: http://localhost:8000")
        print("🔄 Press Ctrl+C to stop")
        print("=" * 50)
        
        # Import the app
        from app import app
        
        # Run the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=["."],
            reload_excludes=["__pycache__", "*.pyc"]
        )
        
    except ImportError:
        print("❌ uvicorn not found!")
        print("Install with: pip install uvicorn")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 