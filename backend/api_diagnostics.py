import os
import sys
import requests
import socket
import json

def detailed_endpoint_diagnosis(base_url='http://127.0.0.1:5000'):
    """
    Comprehensive API endpoint diagnosis
    """
    print("🔬 Detailed API Endpoint Diagnosis")
    print("----------------------------------")

    # Endpoints to diagnose
    endpoints = [
        ('/', 'GET', "Root Endpoint"),
        ('/auth/login', 'POST', "Login Endpoint"),
        ('/auth/register', 'POST', "Registration Endpoint"),
        ('/auth/logout', 'POST', "Logout Endpoint")
    ]

    # Network connectivity check
    try:
        socket.create_connection(("127.0.0.1", 5000), timeout=5)
        print("✅ Network: Local server port is accessible")
    except (socket.error, socket.timeout):
        print("❌ Network: Cannot connect to local server")
        return False

    # Detailed endpoint testing
    for path, method, description in endpoints:
        full_url = f'{base_url}{path}'
        print(f"\n🔍 Diagnosing {description}:")
        print(f"   URL: {full_url}")
        print(f"   Method: {method}")

        try:
            # Perform request with extended timeout and headers
            headers = {
                'User-Agent': 'Coinage API Diagnostic Tool',
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json'
            }
            
            # Different payload for different routes
            payload = {}
            if path == '/auth/login':
                payload = {'username': 'test_user', 'password': 'test_password'}
            elif path == '/auth/register':
                payload = {
                    'username': 'diagnostic_user', 
                    'email': 'diagnostic@test.com', 
                    'password': 'test_password'
                }
            
            if method == 'GET':
                response = requests.get(full_url, headers=headers, timeout=10)
            else:
                response = requests.post(full_url, headers=headers, json=payload, timeout=10)

            # Detailed response analysis
            print(f"   Status Code: {response.status_code}")
            print("   Response Headers:")
            for header, value in response.headers.items():
                print(f"   - {header}: {value}")

            # Content type handling
            content_type = response.headers.get('Content-Type', '')
            print(f"\n   Content Type: {content_type}")

            # JSON parsing
            if 'application/json' in content_type:
                try:
                    json_response = response.json()
                    print("   JSON Response (first 3 keys):")
                    for key in list(json_response.keys())[:3]:
                        print(f"   - {key}: {json_response[key]}")
                except ValueError:
                    print("   ❌ Unable to parse JSON response")

            # Fallback text parsing
            else:
                print("   Response Text (first 200 chars):")
                print(response.text[:200])

        except requests.RequestException as e:
            print(f"   ❌ Request Error: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected Error: {e}")

    return True

def main():
    """
    Main diagnostic entry point
    """
    diagnosis_result = detailed_endpoint_diagnosis()
    sys.exit(0 if diagnosis_result else 1)

if __name__ == '__main__':
    main()
