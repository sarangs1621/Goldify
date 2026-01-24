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
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"  Login Status: {response.status_code}")

if response.status_code != 200:
    print(f"  Error: {response.text}")
    exit(1)

# Get the cookie
cookies = response.cookies
print(f"  Cookies: {dict(cookies)}")

# Test inventory headers
print("\n[2] Testing /api/inventory/headers...")
response = requests.get(f"{BASE_URL}/inventory/headers", cookies=cookies)
print(f"  Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"  Headers count: {len(data)}")
    if len(data) > 0:
        print(f"  Sample header (first 3 fields):")
        sample = data[0]
        for key in list(sample.keys())[:5]:
            print(f"    {key}: {sample[key]}")
else:
    print(f"  Error: {response.text}")

# Test stock totals
print("\n[3] Testing /api/inventory/stock-totals...")
response = requests.get(f"{BASE_URL}/inventory/stock-totals", cookies=cookies)
print(f"  Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"  Stock totals count: {len(data)}")
    if len(data) > 0:
        print(f"  Sample item:")
        sample = data[0]
        for key, value in sample.items():
            print(f"    {key}: {value}")
        total_weight = sum(item.get('total_weight', 0) for item in data)
        total_qty = sum(item.get('total_qty', 0) for item in data)
        print(f"  Total quantity: {total_qty}")
        print(f"  Total weight: {total_weight}g")
else:
    print(f"  Error: {response.text}")

# Test outstanding summary
print("\n[4] Testing /api/parties/outstanding-summary...")
response = requests.get(f"{BASE_URL}/parties/outstanding-summary", cookies=cookies)
print(f"  Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"  Outstanding data:")
    for key, value in data.items():
        print(f"    {key}: {value}")
else:
    print(f"  Error: {response.text}")

print("\n" + "=" * 80)
print("✅ API TESTING COMPLETE")
print("=" * 80)
