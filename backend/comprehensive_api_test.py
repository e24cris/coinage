import requests
import json

def test_comprehensive_api():
    """
    Comprehensive API testing script
    """
    BASE_URL = 'http://127.0.0.1:5000'
    
    print("🌐 Comprehensive API Testing")
    print("----------------------------")
    
    # Test Endpoints
    endpoints = [
        ('/', 'GET', "Home/Root Endpoint"),
        ('/login', 'GET', "Login Page"),
        ('/register', 'GET', "Registration Page"),
        ('/logout', 'GET', "Logout Endpoint"),
    ]
    
    for endpoint, method, description in endpoints:
        try:
            full_url = f'{BASE_URL}{endpoint}'
            print(f"\n🔍 Testing {description}:")
            print(f"   URL: {full_url}")
            print(f"   Method: {method}")
            
            if method == 'GET':
                response = requests.get(full_url, timeout=5)
            else:
                response = requests.post(full_url, timeout=5)
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Headers: {dict(response.headers)}")
            
            # Try to parse and print response content
            try:
                response_content = response.json()
                print("   Response Body (JSON):")
                print(json.dumps(response_content, indent=2)[:500] + "...")
            except (ValueError, TypeError):
                print(f"   Response Text: {response.text[:500]}...")
            
        except requests.RequestException as e:
            print(f"❌ Request Error for {endpoint}: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error for {endpoint}: {e}")

def main():
    """
    Main entry point for API testing
    """
    test_comprehensive_api()

if __name__ == '__main__':
    main()
