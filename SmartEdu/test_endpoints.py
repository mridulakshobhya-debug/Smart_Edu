#!/usr/bin/env python
"""Test script to verify all pages are loading"""
import requests
import time
import sys

# Wait a bit for server to be ready
time.sleep(2)

base_url = "http://127.0.0.1:5000"
endpoints = [
    ("/", "Homepage"),
    ("/elearning/", "E-Learning"),
    ("/elibrary/", "E-Library"),
    ("/auth/login", "Login"),
    ("/auth/signup", "Sign Up"),
    ("/ai", "AI Chatbot"),
]

print("\n📊 Testing SmartEdu Platform Endpoints\n")
print("=" * 50)

for endpoint, name in endpoints:
    try:
        response = requests.get(f"{base_url}{endpoint}", timeout=5)
        status = "✓" if response.status_code == 200 else "✗"
        print(f"{status} {name:20} [{response.status_code}]")
    except Exception as e:
        print(f"✗ {name:20} [ERROR: {str(e)}]")

print("=" * 50)
print("\n✓ Testing complete!\n")
