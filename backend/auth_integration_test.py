import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def test_authentication_flow():
    """
    Comprehensive authentication workflow testing
    """
    print("🔐 Authentication Integration Test")
    print("----------------------------------")

    # Registration Test
    print("\n🆕 User Registration Test:")
    register_payload = {
        'username': 'test_user',
        'email': 'test_user@coinage.com',
        'password': 'secure_password123'
    }
    
    try:
        register_response = requests.post(f'{BASE_URL}/auth/register', json=register_payload)
        print(f"   Registration Status: {register_response.status_code}")
        print("   Response:")
        print(json.dumps(register_response.json(), indent=2))
    except Exception as e:
        print(f"   ❌ Registration Error: {e}")

    # Login Test
    print("\n🔑 User Login Test:")
    login_payload = {
        'username': 'test_user',
        'password': 'secure_password123'
    }
    
    try:
        login_response = requests.post(f'{BASE_URL}/auth/login', json=login_payload)
        print(f"   Login Status: {login_response.status_code}")
        print("   Response:")
        print(json.dumps(login_response.json(), indent=2))
    except Exception as e:
        print(f"   ❌ Login Error: {e}")

    # Logout Test
    print("\n🚪 User Logout Test:")
    try:
        logout_response = requests.post(f'{BASE_URL}/auth/logout')
        print(f"   Logout Status: {logout_response.status_code}")
        print("   Response:")
        print(json.dumps(logout_response.json(), indent=2))
    except Exception as e:
        print(f"   ❌ Logout Error: {e}")

def main():
    """
    Main entry point for authentication testing
    """
    test_authentication_flow()

if __name__ == '__main__':
    main()
