#!/usr/bin/env python3
"""
Test script for Gold Ledger (Party Gold Balance System) - Module 1/10
Tests all gold ledger endpoints and gold balance calculations
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8001/api"

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠ {message}{RESET}")

# Test results tracking
total_tests = 0
passed_tests = 0

def run_test(test_name, test_func):
    global total_tests, passed_tests
    total_tests += 1
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST {total_tests}: {test_name}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}")
    try:
        result = test_func()
        if result:
            passed_tests += 1
            print_success(f"TEST PASSED: {test_name}")
        else:
            print_error(f"TEST FAILED: {test_name}")
        return result
    except Exception as e:
        print_error(f"TEST EXCEPTION: {test_name}")
        print_error(f"Error: {str(e)}")
        return False

def login():
    """Login and get auth token"""
    print_info("Logging in as admin...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print_success(f"Login successful. Token: {token[:20]}...")
        return token
    else:
        print_error(f"Login failed: {response.status_code} - {response.text}")
        return None

def test_create_test_party(token):
    """Create a test party for gold ledger testing"""
    print_info("Creating test party...")
    
    party_data = {
        "name": f"Gold Test Party {datetime.now().strftime('%Y%m%d%H%M%S')}",
        "phone": "1234567890",
        "address": "123 Test Street",
        "party_type": "customer",
        "notes": "Test party for gold ledger"
    }
    
    response = requests.post(
        f"{BASE_URL}/parties",
        headers={"Authorization": f"Bearer {token}"},
        json=party_data
    )
    
    if response.status_code == 200:
        party = response.json()
        print_success(f"Party created: {party['name']} (ID: {party['id']})")
        return party['id']
    else:
        print_error(f"Party creation failed: {response.status_code} - {response.text}")
        return None

def test_create_gold_ledger_in_entry(token, party_id):
    """Test creating IN entry (shop receives gold from party)"""
    print_info("Creating IN entry (party gives gold to shop)...")
    
    entry_data = {
        "party_id": party_id,
        "type": "IN",
        "weight_grams": 125.456,  # Testing 3 decimal precision
        "purity_entered": 22,
        "purpose": "advance_gold",
        "reference_type": "manual",
        "notes": "Test IN entry - party gave gold to shop"
    }
    
    response = requests.post(
        f"{BASE_URL}/gold-ledger",
        headers={"Authorization": f"Bearer {token}"},
        json=entry_data
    )
    
    if response.status_code == 200:
        entry = response.json()
        print_success(f"IN entry created successfully")
        print_info(f"  Entry ID: {entry['id']}")
        print_info(f"  Weight: {entry['weight_grams']} grams (should be rounded to 3 decimals)")
        print_info(f"  Type: {entry['type']}")
        print_info(f"  Purpose: {entry['purpose']}")
        
        # Verify 3 decimal precision
        if entry['weight_grams'] == 125.456:
            print_success("✓ Weight precision is correct (3 decimals)")
            return entry['id']
        else:
            print_error(f"✗ Weight precision issue: expected 125.456, got {entry['weight_grams']}")
            return None
    else:
        print_error(f"IN entry creation failed: {response.status_code} - {response.text}")
        return None

def test_create_gold_ledger_out_entry(token, party_id):
    """Test creating OUT entry (shop gives gold to party)"""
    print_info("Creating OUT entry (shop gives gold to party)...")
    
    entry_data = {
        "party_id": party_id,
        "type": "OUT",
        "weight_grams": 50.123,  # Testing 3 decimal precision
        "purity_entered": 22,
        "purpose": "job_work",
        "reference_type": "jobcard",
        "notes": "Test OUT entry - shop gave gold to party for job work"
    }
    
    response = requests.post(
        f"{BASE_URL}/gold-ledger",
        headers={"Authorization": f"Bearer {token}"},
        json=entry_data
    )
    
    if response.status_code == 200:
        entry = response.json()
        print_success(f"OUT entry created successfully")
        print_info(f"  Entry ID: {entry['id']}")
        print_info(f"  Weight: {entry['weight_grams']} grams")
        print_info(f"  Type: {entry['type']}")
        print_info(f"  Purpose: {entry['purpose']}")
        
        # Verify 3 decimal precision
        if entry['weight_grams'] == 50.123:
            print_success("✓ Weight precision is correct (3 decimals)")
            return entry['id']
        else:
            print_error(f"✗ Weight precision issue: expected 50.123, got {entry['weight_grams']}")
            return None
    else:
        print_error(f"OUT entry creation failed: {response.status_code} - {response.text}")
        return None

def test_get_all_gold_ledger_entries(token):
    """Test getting all gold ledger entries"""
    print_info("Getting all gold ledger entries...")
    
    response = requests.get(
        f"{BASE_URL}/gold-ledger",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        entries = response.json()
        print_success(f"Retrieved {len(entries)} gold ledger entries")
        
        for i, entry in enumerate(entries[:5], 1):  # Show first 5
            print_info(f"  Entry {i}: {entry['type']} - {entry['weight_grams']}g - {entry['purpose']}")
        
        return len(entries) > 0
    else:
        print_error(f"Failed to get entries: {response.status_code} - {response.text}")
        return False

def test_get_gold_ledger_by_party(token, party_id):
    """Test filtering gold ledger entries by party_id"""
    print_info(f"Getting gold ledger entries for party {party_id[:8]}...")
    
    response = requests.get(
        f"{BASE_URL}/gold-ledger?party_id={party_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        entries = response.json()
        print_success(f"Retrieved {len(entries)} entries for this party")
        
        # Verify all entries are for the correct party
        all_correct = all(entry['party_id'] == party_id for entry in entries)
        if all_correct:
            print_success("✓ All entries belong to the correct party")
        else:
            print_error("✗ Some entries belong to wrong party")
            return False
        
        return len(entries) >= 2  # Should have at least 2 entries (IN and OUT)
    else:
        print_error(f"Failed to get entries by party: {response.status_code} - {response.text}")
        return False

def test_get_gold_ledger_by_date_range(token):
    """Test filtering gold ledger entries by date range"""
    print_info("Getting gold ledger entries for today...")
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    response = requests.get(
        f"{BASE_URL}/gold-ledger?date_from={today}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        entries = response.json()
        print_success(f"Retrieved {len(entries)} entries from {today}")
        return len(entries) >= 2
    else:
        print_error(f"Failed to get entries by date: {response.status_code} - {response.text}")
        return False

def test_party_gold_summary(token, party_id):
    """Test getting party gold balance summary"""
    print_info(f"Getting gold summary for party {party_id[:8]}...")
    
    response = requests.get(
        f"{BASE_URL}/parties/{party_id}/gold-summary",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        summary = response.json()
        print_success("Gold summary retrieved successfully")
        print_info(f"  Party: {summary['party_name']}")
        print_info(f"  Gold Due FROM Party (party owes shop): {summary['gold_due_from_party']} grams")
        print_info(f"  Gold Due TO Party (shop owes party): {summary['gold_due_to_party']} grams")
        print_info(f"  Net Gold Balance: {summary['net_gold_balance']} grams")
        print_info(f"  Total Entries: {summary['total_entries']}")
        
        # Verify calculations
        # IN = 125.456 grams (party gave to shop)
        # OUT = 50.123 grams (shop gave to party)
        # Net = 125.456 - 50.123 = 75.333 grams (party owes shop)
        
        expected_due_from = 125.456
        expected_due_to = 50.123
        expected_net = round(125.456 - 50.123, 3)
        
        if summary['gold_due_from_party'] == expected_due_from:
            print_success(f"✓ Gold due from party is correct: {expected_due_from}g")
        else:
            print_error(f"✗ Gold due from party incorrect: expected {expected_due_from}, got {summary['gold_due_from_party']}")
            return False
        
        if summary['gold_due_to_party'] == expected_due_to:
            print_success(f"✓ Gold due to party is correct: {expected_due_to}g")
        else:
            print_error(f"✗ Gold due to party incorrect: expected {expected_due_to}, got {summary['gold_due_to_party']}")
            return False
        
        if summary['net_gold_balance'] == expected_net:
            print_success(f"✓ Net gold balance is correct: {expected_net}g")
        else:
            print_error(f"✗ Net gold balance incorrect: expected {expected_net}, got {summary['net_gold_balance']}")
            return False
        
        return True
    else:
        print_error(f"Failed to get gold summary: {response.status_code} - {response.text}")
        return False

def test_delete_gold_ledger_entry(token, entry_id):
    """Test soft deleting a gold ledger entry"""
    print_info(f"Deleting gold ledger entry {entry_id[:8]}...")
    
    response = requests.delete(
        f"{BASE_URL}/gold-ledger/{entry_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        print_success("Entry deleted successfully (soft delete)")
        
        # Verify entry is soft deleted (should not appear in GET)
        response = requests.get(
            f"{BASE_URL}/gold-ledger",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            entries = response.json()
            deleted_entry = next((e for e in entries if e['id'] == entry_id), None)
            
            if deleted_entry is None:
                print_success("✓ Deleted entry does not appear in listing (soft delete working)")
                return True
            else:
                print_error("✗ Deleted entry still appears in listing")
                return False
        
        return True
    else:
        print_error(f"Failed to delete entry: {response.status_code} - {response.text}")
        return False

def test_validation_invalid_type(token, party_id):
    """Test validation - invalid type"""
    print_info("Testing validation: invalid type...")
    
    entry_data = {
        "party_id": party_id,
        "type": "INVALID",  # Should fail
        "weight_grams": 100.0,
        "purity_entered": 22,
        "purpose": "job_work"
    }
    
    response = requests.post(
        f"{BASE_URL}/gold-ledger",
        headers={"Authorization": f"Bearer {token}"},
        json=entry_data
    )
    
    if response.status_code == 400:
        print_success("✓ Validation working: invalid type rejected")
        return True
    else:
        print_error(f"✗ Validation failed: invalid type was accepted (status: {response.status_code})")
        return False

def test_validation_invalid_purpose(token, party_id):
    """Test validation - invalid purpose"""
    print_info("Testing validation: invalid purpose...")
    
    entry_data = {
        "party_id": party_id,
        "type": "IN",
        "weight_grams": 100.0,
        "purity_entered": 22,
        "purpose": "invalid_purpose"  # Should fail
    }
    
    response = requests.post(
        f"{BASE_URL}/gold-ledger",
        headers={"Authorization": f"Bearer {token}"},
        json=entry_data
    )
    
    if response.status_code == 400:
        print_success("✓ Validation working: invalid purpose rejected")
        return True
    else:
        print_error(f"✗ Validation failed: invalid purpose was accepted (status: {response.status_code})")
        return False

def test_validation_missing_party(token):
    """Test validation - party not found"""
    print_info("Testing validation: non-existent party...")
    
    entry_data = {
        "party_id": "non-existent-party-id",
        "type": "IN",
        "weight_grams": 100.0,
        "purity_entered": 22,
        "purpose": "job_work"
    }
    
    response = requests.post(
        f"{BASE_URL}/gold-ledger",
        headers={"Authorization": f"Bearer {token}"},
        json=entry_data
    )
    
    if response.status_code == 404:
        print_success("✓ Validation working: non-existent party rejected")
        return True
    else:
        print_error(f"✗ Validation failed: non-existent party was accepted (status: {response.status_code})")
        return False

def main():
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}GOLD LEDGER MODULE TEST SUITE - MODULE 1/10{RESET}")
    print(f"{BLUE}Testing: Gold Ledger (Party Gold Balance System){RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    # Login
    token = login()
    if not token:
        print_error("Failed to login. Exiting.")
        return
    
    # Create test party
    party_id = test_create_test_party(token)
    if not party_id:
        print_error("Failed to create test party. Exiting.")
        return
    
    # Run all tests
    in_entry_id = None
    out_entry_id = None
    
    def test_1():
        nonlocal in_entry_id
        in_entry_id = test_create_gold_ledger_in_entry(token, party_id)
        return in_entry_id is not None
    
    def test_2():
        nonlocal out_entry_id
        out_entry_id = test_create_gold_ledger_out_entry(token, party_id)
        return out_entry_id is not None
    
    run_test("Create IN Entry (Party Gives Gold to Shop)", test_1)
    run_test("Create OUT Entry (Shop Gives Gold to Party)", test_2)
    run_test("Get All Gold Ledger Entries", lambda: test_get_all_gold_ledger_entries(token))
    run_test("Filter Entries by Party ID", lambda: test_get_gold_ledger_by_party(token, party_id))
    run_test("Filter Entries by Date Range", lambda: test_get_gold_ledger_by_date_range(token))
    run_test("Get Party Gold Summary with Balance Calculation", lambda: test_party_gold_summary(token, party_id))
    
    if in_entry_id:
        run_test("Soft Delete Gold Ledger Entry", lambda: test_delete_gold_ledger_entry(token, in_entry_id))
    
    run_test("Validation: Reject Invalid Type", lambda: test_validation_invalid_type(token, party_id))
    run_test("Validation: Reject Invalid Purpose", lambda: test_validation_invalid_purpose(token, party_id))
    run_test("Validation: Reject Non-existent Party", lambda: test_validation_missing_party(token))
    
    # Print summary
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST SUMMARY{RESET}")
    print(f"{BLUE}{'='*80}{RESET}")
    print(f"Total Tests: {total_tests}")
    print(f"{GREEN}Passed: {passed_tests}{RESET}")
    print(f"{RED}Failed: {total_tests - passed_tests}{RESET}")
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")
    
    if passed_tests == total_tests:
        print(f"\n{GREEN}{'='*80}{RESET}")
        print(f"{GREEN}🎉 ALL TESTS PASSED! GOLD LEDGER MODULE IS WORKING PERFECTLY! 🎉{RESET}")
        print(f"{GREEN}{'='*80}{RESET}\n")
    else:
        print(f"\n{YELLOW}{'='*80}{RESET}")
        print(f"{YELLOW}⚠ SOME TESTS FAILED. PLEASE REVIEW THE OUTPUT ABOVE. ⚠{RESET}")
        print(f"{YELLOW}{'='*80}{RESET}\n")

if __name__ == "__main__":
    main()
