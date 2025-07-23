#!/usr/bin/env python3
"""
Minimal test script to debug run issues
"""

import sys
import traceback

print("🧪 Testing Privacy.com FastAPI Application")
print("=" * 50)

# Test 1: Basic Python imports
print("1. Testing basic imports...")
try:
    import os
    import json
    import datetime
    import secrets
    import logging
    print("   ✅ Basic Python modules OK")
except Exception as e:
    print(f"   ❌ Basic imports failed: {e}")
    sys.exit(1)

# Test 2: FastAPI imports
print("\n2. Testing FastAPI imports...")
try:
    import fastapi
    print(f"   ✅ FastAPI version: {fastapi.__version__}")
except Exception as e:
    print(f"   ❌ FastAPI not found: {e}")
    print("   Install with: pip install fastapi")
    sys.exit(1)

# Test 3: Uvicorn imports
print("\n3. Testing Uvicorn imports...")
try:
    import uvicorn
    print(f"   ✅ Uvicorn available")
except Exception as e:
    print(f"   ❌ Uvicorn not found: {e}")
    print("   Install with: pip install uvicorn")
    sys.exit(1)

# Test 4: Other dependencies
print("\n4. Testing other dependencies...")
try:
    import jinja2
    print(f"   ✅ Jinja2 available")
except Exception as e:
    print(f"   ❌ Jinja2 not found: {e}")
    print("   Install with: pip install jinja2")

try:
    import requests
    print(f"   ✅ Requests available")
except Exception as e:
    print(f"   ❌ Requests not found: {e}")
    print("   Install with: pip install requests")

# Test 5: App import
print("\n5. Testing app import...")
try:
    from app import app
    print("   ✅ App imported successfully")
    print(f"   ✅ App type: {type(app)}")
except Exception as e:
    print(f"   ❌ App import failed: {e}")
    print("\n   Full traceback:")
    traceback.print_exc()
    sys.exit(1)

# Test 6: Try to start server (just test, don't actually run)
print("\n6. Testing server configuration...")
try:
    # Just test the configuration, don't actually run
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
    print("   ✅ Server configuration OK")
except Exception as e:
    print(f"   ❌ Server configuration failed: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n🎉 All tests passed! The app should be able to run.")
print("Try running: python run.py")
print("Or directly: uvicorn app:app --reload") 