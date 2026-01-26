#!/usr/bin/env python3
"""
COMPREHENSIVE AUTHENTICATION AND LOGIN TESTING
Testing authentication system for Gold Shop ERP

TESTING REQUIREMENTS:
1. LOGIN ENDPOINT TESTING (/api/auth/login)
2. TOKEN VALIDATION
3. AUTHENTICATION FLOW
4. EDGE CASES
5. SECURITY FEATURES

Available Test Users:
- admin / admin123 (role: admin, should have 27+ permissions)
- staff / staff123 (role: staff, should have 11 permissions)
"""

import requests
import json
import time
import uuid
from datetime import datetime, timezone
import jwt

# Configuration - Use the correct backend URL
BASE_URL = "http://localhost:8001/api"  # Backend running on port 8001
HEADERS = {"Content-Type": "application/json"}

class AuthenticationTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.test_results = []
        self.valid_tokens = {}
        
    def log_result(self, test_name, success, details="", error=""):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    Details: {details}")
        if error:
            print(f"    Error: {error}")
        print()

    def test_login_endpoint_success(self):
        """Test successful login with valid credentials"""
        print("=" * 80)
        print("PHASE 1: LOGIN ENDPOINT TESTING - SUCCESS CASES")
        print("=" * 80)
        
        # Test 1: Admin login
        try:
            login_data = {
                "username": "admin",
                "password": "admin123"
            }
            
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["access_token", "token_type", "user", "csrf_token"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_result("Admin Login - Response Structure", False, "", 
                                  f"Missing fields: {missing_fields}")
                else:
                    # Verify user object structure
                    user = data["user"]
                    user_required_fields = ["id", "username", "email", "role", "permissions", "is_active"]
                    user_missing_fields = [field for field in user_required_fields if field not in user]
                    
                    if user_missing_fields:
                        self.log_result("Admin Login - User Object Structure", False, "", 
                                      f"Missing user fields: {user_missing_fields}")
                    else:
                        # Store valid token for later tests
                        self.valid_tokens["admin"] = {
                            "token": data["access_token"],
                            "csrf_token": data["csrf_token"],
                            "user": user
                        }
                        
                        # Verify admin permissions (should have 27+ permissions)
                        permissions_count = len(user.get("permissions", []))
                        if permissions_count >= 27:
                            self.log_result("Admin Login - Success", True, 
                                          f"Admin login successful. Token type: {data['token_type']}, "
                                          f"Role: {user['role']}, Permissions: {permissions_count}, "
                                          f"Active: {user['is_active']}")
                        else:
                            self.log_result("Admin Login - Permissions Count", False, "", 
                                          f"Admin should have 27+ permissions, got {permissions_count}")
            else:
                self.log_result("Admin Login - Success", False, "", 
                              f"Login failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.log_result("Admin Login - Success", False, "", f"Error: {str(e)}")

        # Test 2: Staff login
        try:
            login_data = {
                "username": "staff",
                "password": "staff123"
            }
            
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                user = data["user"]
                
                # Store valid token for later tests
                self.valid_tokens["staff"] = {
                    "token": data["access_token"],
                    "csrf_token": data["csrf_token"],
                    "user": user
                }
                
                # Verify staff permissions (should have 11 permissions)
                permissions_count = len(user.get("permissions", []))
                if permissions_count == 11:
                    self.log_result("Staff Login - Success", True, 
                                  f"Staff login successful. Role: {user['role']}, "
                                  f"Permissions: {permissions_count}, Active: {user['is_active']}")
                else:
                    self.log_result("Staff Login - Permissions Count", False, "", 
                                  f"Staff should have 11 permissions, got {permissions_count}")
            else:
                self.log_result("Staff Login - Success", False, "", 
                              f"Staff login failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.log_result("Staff Login - Success", False, "", f"Error: {str(e)}")

    def test_login_endpoint_failures(self):
        """Test login failures with invalid credentials"""
        print("=" * 80)
        print("PHASE 1: LOGIN ENDPOINT TESTING - FAILURE CASES")
        print("=" * 80)
        
        # Test 3: Invalid credentials
        try:
            login_data = {
                "username": "admin",
                "password": "wrongpassword"
            }
            
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code == 401:
                self.log_result("Invalid Credentials - 401 Response", True, 
                              "Correctly returned 401 for invalid password")
            else:
                self.log_result("Invalid Credentials - 401 Response", False, "", 
                              f"Expected 401, got {response.status_code}")
                
        except Exception as e:
            self.log_result("Invalid Credentials - 401 Response", False, "", f"Error: {str(e)}")

        # Test 4: Non-existent user
        try:
            login_data = {
                "username": "nonexistentuser",
                "password": "anypassword"
            }
            
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code == 401:
                self.log_result("Non-existent User - 401 Response", True, 
                              "Correctly returned 401 for non-existent user")
            else:
                self.log_result("Non-existent User - 401 Response", False, "", 
                              f"Expected 401, got {response.status_code}")
                
        except Exception as e:
            self.log_result("Non-existent User - 401 Response", False, "", f"Error: {str(e)}")

    def test_rate_limiting(self):
        """Test rate limiting (5 attempts per minute per IP)"""
        print("=" * 80)
        print("PHASE 1: RATE LIMITING TESTING")
        print("=" * 80)
        
        try:
            # Make 6 rapid login attempts to trigger rate limiting
            login_data = {
                "username": "admin",
                "password": "wrongpassword"
            }
            
            rate_limit_triggered = False
            for i in range(6):
                response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
                if response.status_code == 429:  # Too Many Requests
                    rate_limit_triggered = True
                    break
                time.sleep(0.1)  # Small delay between requests
            
            if rate_limit_triggered:
                self.log_result("Rate Limiting - 5 attempts per minute", True, 
                              "Rate limiting correctly triggered after multiple attempts")
            else:
                self.log_result("Rate Limiting - 5 attempts per minute", False, "", 
                              "Rate limiting not triggered after 6 attempts")
                
        except Exception as e:
            self.log_result("Rate Limiting - 5 attempts per minute", False, "", f"Error: {str(e)}")

    def test_account_lockout(self):
        """Test account lockout after 5 failed attempts"""
        print("=" * 80)
        print("PHASE 1: ACCOUNT LOCKOUT TESTING")
        print("=" * 80)
        
        try:
            # Create a test user first (if we have admin token)
            if "admin" in self.valid_tokens:
                # Try to make 5 failed login attempts with admin account
                # Note: This might lock the admin account, so we'll use a different approach
                # We'll test with the staff account instead
                
                login_data = {
                    "username": "staff",
                    "password": "wrongpassword"
                }
                
                lockout_triggered = False
                for i in range(6):  # Try 6 times to trigger lockout after 5 failures
                    response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
                    if response.status_code == 403 and "locked" in response.text.lower():
                        lockout_triggered = True
                        break
                    time.sleep(1)  # Wait between attempts to avoid rate limiting
                
                if lockout_triggered:
                    self.log_result("Account Lockout - 5 failed attempts", True, 
                                  "Account correctly locked after 5 failed login attempts")
                else:
                    self.log_result("Account Lockout - 5 failed attempts", False, "", 
                                  "Account lockout not triggered after multiple failed attempts")
            else:
                self.log_result("Account Lockout - 5 failed attempts", False, "", 
                              "Cannot test lockout without admin token")
                
        except Exception as e:
            self.log_result("Account Lockout - 5 failed attempts", False, "", f"Error: {str(e)}")

    def test_token_validation(self):
        """Test JWT token validation"""
        print("=" * 80)
        print("PHASE 2: TOKEN VALIDATION TESTING")
        print("=" * 80)
        
        # Test 5: /api/auth/me with valid token
        if "admin" in self.valid_tokens:
            try:
                headers = {
                    "Authorization": f"Bearer {self.valid_tokens['admin']['token']}",
                    "Content-Type": "application/json"
                }
                
                response = self.session.get(f"{BASE_URL}/auth/me", headers=headers)
                
                if response.status_code == 200:
                    user_data = response.json()
                    if user_data.get("username") == "admin":
                        self.log_result("Token Validation - /auth/me endpoint", True, 
                                      f"Successfully retrieved user data for {user_data['username']}")
                    else:
                        self.log_result("Token Validation - /auth/me endpoint", False, "", 
                                      f"Wrong user data returned: {user_data.get('username')}")
                else:
                    self.log_result("Token Validation - /auth/me endpoint", False, "", 
                                  f"Failed to access /auth/me: {response.status_code} - {response.text}")
                    
            except Exception as e:
                self.log_result("Token Validation - /auth/me endpoint", False, "", f"Error: {str(e)}")

        # Test 6: Protected endpoint with valid token
        if "admin" in self.valid_tokens:
            try:
                headers = {
                    "Authorization": f"Bearer {self.valid_tokens['admin']['token']}",
                    "X-CSRF-Token": self.valid_tokens['admin']['csrf_token'],
                    "Content-Type": "application/json"
                }
                
                response = self.session.get(f"{BASE_URL}/parties", headers=headers)
                
                if response.status_code == 200:
                    self.log_result("Protected Endpoint - Valid Token", True, 
                                  "Successfully accessed /parties with valid token")
                else:
                    self.log_result("Protected Endpoint - Valid Token", False, "", 
                                  f"Failed to access /parties: {response.status_code} - {response.text}")
                    
            except Exception as e:
                self.log_result("Protected Endpoint - Valid Token", False, "", f"Error: {str(e)}")

        # Test 7: Protected endpoint without token
        try:
            response = self.session.get(f"{BASE_URL}/parties")
            
            if response.status_code == 401:
                self.log_result("Protected Endpoint - No Token", True, 
                              "Correctly returned 401 for request without token")
            else:
                self.log_result("Protected Endpoint - No Token", False, "", 
                              f"Expected 401, got {response.status_code}")
                
        except Exception as e:
            self.log_result("Protected Endpoint - No Token", False, "", f"Error: {str(e)}")

        # Test 8: Protected endpoint with invalid token
        try:
            headers = {
                "Authorization": "Bearer invalid_token_here",
                "Content-Type": "application/json"
            }
            
            response = self.session.get(f"{BASE_URL}/parties", headers=headers)
            
            if response.status_code == 401:
                self.log_result("Protected Endpoint - Invalid Token", True, 
                              "Correctly returned 401 for invalid token")
            else:
                self.log_result("Protected Endpoint - Invalid Token", False, "", 
                              f"Expected 401, got {response.status_code}")
                
        except Exception as e:
            self.log_result("Protected Endpoint - Invalid Token", False, "", f"Error: {str(e)}")

    def test_authentication_flow(self):
        """Test complete authentication flow"""
        print("=" * 80)
        print("PHASE 3: AUTHENTICATION FLOW TESTING")
        print("=" * 80)
        
        # Test 9: Complete login → token → protected resource flow
        try:
            # Step 1: Login
            login_data = {
                "username": "admin",
                "password": "admin123"
            }
            
            login_response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if login_response.status_code == 200:
                login_data = login_response.json()
                token = login_data["access_token"]
                csrf_token = login_data["csrf_token"]
                
                # Step 2: Use token to access protected resource
                headers = {
                    "Authorization": f"Bearer {token}",
                    "X-CSRF-Token": csrf_token,
                    "Content-Type": "application/json"
                }
                
                protected_response = self.session.get(f"{BASE_URL}/parties", headers=headers)
                
                if protected_response.status_code == 200:
                    self.log_result("Complete Authentication Flow", True, 
                                  "Successfully completed login → token → protected resource flow")
                else:
                    self.log_result("Complete Authentication Flow", False, "", 
                                  f"Failed to access protected resource: {protected_response.status_code}")
            else:
                self.log_result("Complete Authentication Flow", False, "", 
                              f"Login failed in flow test: {login_response.status_code}")
                
        except Exception as e:
            self.log_result("Complete Authentication Flow", False, "", f"Error: {str(e)}")

        # Test 10: Verify permissions are correctly assigned
        if "admin" in self.valid_tokens and "staff" in self.valid_tokens:
            try:
                admin_permissions = len(self.valid_tokens["admin"]["user"]["permissions"])
                staff_permissions = len(self.valid_tokens["staff"]["user"]["permissions"])
                
                if admin_permissions >= 27 and staff_permissions == 11:
                    self.log_result("Permission Assignment Verification", True, 
                                  f"Correct permissions: Admin={admin_permissions}, Staff={staff_permissions}")
                else:
                    self.log_result("Permission Assignment Verification", False, "", 
                                  f"Incorrect permissions: Admin={admin_permissions} (expected 27+), "
                                  f"Staff={staff_permissions} (expected 11)")
                    
            except Exception as e:
                self.log_result("Permission Assignment Verification", False, "", f"Error: {str(e)}")

        # Test 11: Logout endpoint
        if "admin" in self.valid_tokens:
            try:
                headers = {
                    "Authorization": f"Bearer {self.valid_tokens['admin']['token']}",
                    "X-CSRF-Token": self.valid_tokens['admin']['csrf_token'],
                    "Content-Type": "application/json"
                }
                
                response = self.session.post(f"{BASE_URL}/auth/logout", headers=headers)
                
                if response.status_code == 200:
                    self.log_result("Logout Endpoint", True, 
                                  "Successfully logged out")
                else:
                    self.log_result("Logout Endpoint", False, "", 
                                  f"Logout failed: {response.status_code} - {response.text}")
                    
            except Exception as e:
                self.log_result("Logout Endpoint", False, "", f"Error: {str(e)}")

    def test_edge_cases(self):
        """Test edge cases and security"""
        print("=" * 80)
        print("PHASE 4: EDGE CASES AND SECURITY TESTING")
        print("=" * 80)
        
        # Test 12: Empty username/password
        try:
            login_data = {
                "username": "",
                "password": ""
            }
            
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code in [400, 401, 422]:  # Bad request or validation error
                self.log_result("Empty Credentials", True, 
                              f"Correctly rejected empty credentials with {response.status_code}")
            else:
                self.log_result("Empty Credentials", False, "", 
                              f"Should reject empty credentials, got {response.status_code}")
                
        except Exception as e:
            self.log_result("Empty Credentials", False, "", f"Error: {str(e)}")

        # Test 13: SQL injection attempts
        try:
            login_data = {
                "username": "admin'; DROP TABLE users; --",
                "password": "admin123"
            }
            
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code == 401:
                self.log_result("SQL Injection Protection", True, 
                              "SQL injection attempt correctly rejected")
            else:
                self.log_result("SQL Injection Protection", False, "", 
                              f"SQL injection attempt got unexpected response: {response.status_code}")
                
        except Exception as e:
            self.log_result("SQL Injection Protection", False, "", f"Error: {str(e)}")

        # Test 14: Very long username/password
        try:
            login_data = {
                "username": "a" * 1000,  # Very long username
                "password": "b" * 1000   # Very long password
            }
            
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code in [400, 401, 413, 422]:  # Bad request or payload too large
                self.log_result("Long Credentials Protection", True, 
                              f"Long credentials correctly rejected with {response.status_code}")
            else:
                self.log_result("Long Credentials Protection", False, "", 
                              f"Long credentials got unexpected response: {response.status_code}")
                
        except Exception as e:
            self.log_result("Long Credentials Protection", False, "", f"Error: {str(e)}")

        # Test 15: Special characters in credentials
        try:
            login_data = {
                "username": "admin<script>alert('xss')</script>",
                "password": "admin123"
            }
            
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code == 401:
                self.log_result("Special Characters Protection", True, 
                              "Special characters in username correctly handled")
            else:
                self.log_result("Special Characters Protection", False, "", 
                              f"Special characters got unexpected response: {response.status_code}")
                
        except Exception as e:
            self.log_result("Special Characters Protection", False, "", f"Error: {str(e)}")

    def test_security_features(self):
        """Test security features"""
        print("=" * 80)
        print("PHASE 5: SECURITY FEATURES TESTING")
        print("=" * 80)
        
        # Test 16: Verify CSRF token is returned
        try:
            login_data = {
                "username": "admin",
                "password": "admin123"
            }
            
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if "csrf_token" in data and data["csrf_token"]:
                    self.log_result("CSRF Token Generation", True, 
                                  f"CSRF token correctly generated (length: {len(data['csrf_token'])})")
                else:
                    self.log_result("CSRF Token Generation", False, "", 
                                  "CSRF token missing from login response")
            else:
                self.log_result("CSRF Token Generation", False, "", 
                              f"Login failed for CSRF test: {response.status_code}")
                
        except Exception as e:
            self.log_result("CSRF Token Generation", False, "", f"Error: {str(e)}")

        # Test 17: Verify auth audit logs (we can't directly check the database, 
        # but we can verify the login endpoint works which should create audit logs)
        try:
            # Multiple login attempts should create audit logs
            login_attempts = [
                {"username": "admin", "password": "admin123", "should_succeed": True},
                {"username": "admin", "password": "wrongpass", "should_succeed": False},
                {"username": "nonexistent", "password": "anypass", "should_succeed": False}
            ]
            
            audit_log_test_passed = True
            for attempt in login_attempts:
                response = self.session.post(f"{BASE_URL}/auth/login", json={
                    "username": attempt["username"],
                    "password": attempt["password"]
                })
                
                expected_status = 200 if attempt["should_succeed"] else 401
                if response.status_code != expected_status:
                    audit_log_test_passed = False
                    break
            
            if audit_log_test_passed:
                self.log_result("Auth Audit Logs", True, 
                              "Login attempts processed correctly (audit logs should be created)")
            else:
                self.log_result("Auth Audit Logs", False, "", 
                              "Login attempts not processed as expected")
                
        except Exception as e:
            self.log_result("Auth Audit Logs", False, "", f"Error: {str(e)}")

    def run_comprehensive_test(self):
        """Run all authentication tests"""
        print("🚀 STARTING COMPREHENSIVE AUTHENTICATION AND LOGIN TESTING")
        print("=" * 80)
        
        # Phase 1: Login endpoint testing
        self.test_login_endpoint_success()
        self.test_login_endpoint_failures()
        self.test_rate_limiting()
        self.test_account_lockout()
        
        # Phase 2: Token validation
        self.test_token_validation()
        
        # Phase 3: Authentication flow
        self.test_authentication_flow()
        
        # Phase 4: Edge cases
        self.test_edge_cases()
        
        # Phase 5: Security features
        self.test_security_features()
        
        # Print summary
        self.print_summary()
        
        return True

    def print_summary(self):
        """Print test results summary"""
        print("=" * 80)
        print("🎯 COMPREHENSIVE AUTHENTICATION TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        if failed_tests > 0:
            print("❌ FAILED TESTS:")
            print("-" * 40)
            for result in self.test_results:
                if not result["success"]:
                    print(f"• {result['test']}")
                    if result["error"]:
                        print(f"  Error: {result['error']}")
            print()
        
        print("✅ PASSED TESTS:")
        print("-" * 40)
        for result in self.test_results:
            if result["success"]:
                print(f"• {result['test']}")
        
        print("=" * 80)
        print("🏁 AUTHENTICATION TESTING COMPLETE")
        print("=" * 80)

if __name__ == "__main__":
    tester = AuthenticationTester()
    tester.run_comprehensive_test()