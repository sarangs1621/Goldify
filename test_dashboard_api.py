#!/usr/bin/env python3
"""Test dashboard APIs"""
import requests
import json

BASE_URL = "http://localhost:8001/api"

# First login to get auth cookie
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("=" * 80)
print("DASHBOARD API TESTING")
print("=" * 80)

# Login
print("\n[1] Logging in...")
session = requests.Session()
response = session.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"  Login Status: {response.status_code}")

if response.status_code != 200:
    print(f"  Error: {response.text}")
    exit(1)

# Test inventory headers
print("\n[2] Testing /api/inventory/headers...")
response = session.get(f"{BASE_URL}/inventory/headers")
print(f"  Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"  Headers count: {len(data)}")
    if len(data) > 0:
        print(f"  Sample header: {json.dumps(data[0], indent=2)}")
else:
    print(f"  Error: {response.text}")

# Test stock totals
print("\n[3] Testing /api/inventory/stock-totals...")
response = session.get(f"{BASE_URL}/inventory/stock-totals")
print(f"  Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"  Stock totals count: {len(data)}")
    if len(data) > 0:
        print(f"  Sample item: {json.dumps(data[0], indent=2)}")
        total_weight = sum(item.get('total_weight', 0) for item in data)
        print(f"  Total weight across all categories: {total_weight}g")
else:
    print(f"  Error: {response.text}")

# Test outstanding summary
print("\n[4] Testing /api/parties/outstanding-summary...")
response = session.get(f"{BASE_URL}/parties/outstanding-summary")
print(f"  Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"  Outstanding data: {json.dumps(data, indent=2)}")
else:
    print(f"  Error: {response.text}")

print("\n" + "=" * 80)
print("✅ API TESTING COMPLETE")
print("=" * 80)
