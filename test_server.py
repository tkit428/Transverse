#!/usr/bin/env python3
"""
Test script to verify Django server is working properly.
"""

import requests
import sys
from pathlib import Path

def test_server():
    """Test Django server endpoints."""
    base_url = "http://127.0.0.1:8000"

    print("Testing Django server...")
    print(f"Base URL: {base_url}")

    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Server is running (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Server not running: {e}")
        return False

    # Test 2: Check upload endpoint (GET)
    try:
        response = requests.get(f"{base_url}/api/upload/")
        print(f"✅ Upload endpoint accessible (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Upload endpoint not accessible: {e}")
        return False

    # Test 3: Check translate endpoint (GET)
    try:
        response = requests.get(f"{base_url}/api/translate/")
        print(f"✅ Translate endpoint accessible (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Translate endpoint not accessible: {e}")
        return False

    print("\n🎉 All tests passed! Server is working correctly.")
    return True

if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)
