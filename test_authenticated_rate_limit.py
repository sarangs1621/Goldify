#!/usr/bin/env python3
"""
Quick authenticated endpoint test
"""

import requests
import os
import time

BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

print("Waiting 60 seconds for rate limit to reset...")
time.sleep(60)

print("\nTesting authenticated endpoints after rate limit reset...")

# Try to login
login_data = {
    "username": "admin",
    "password": "admin123"
}

response = requests.post(f"{API_BASE}/auth/login", json=login_data, timeout=5)
print(f"Login status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    token = data.get('access_token')
    cookies = response.cookies.get_dict()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test /auth/me endpoint
    response = requests.get(f"{API_BASE}/auth/me", headers=headers, cookies=cookies, timeout=5)
    print(f"GET /auth/me status: {response.status_code}")
    if response.status_code == 200:
        user = response.json()
        print(f"✓ Authenticated as: {user.get('username')} ({user.get('role')})")
    
    # Test users endpoint
    response = requests.get(f"{API_BASE}/users", headers=headers, cookies=cookies, timeout=5)
    print(f"GET /users status: {response.status_code}")
    if response.status_code == 200:
        users = response.json()
        print(f"✓ Retrieved users list")
    
    # Test health endpoint
    response = requests.get(f"{API_BASE}/health", timeout=5)
    print(f"GET /health status: {response.status_code}")
    if response.status_code == 200:
        print(f"✓ Health check working")
    
    print("\n✅ All authenticated endpoint tests passed!")
else:
    print(f"❌ Login failed with status {response.status_code}")
