import requests

def check_routes():
    """
    Quick route checking while server is running
    """
    BASE_URL = 'http://127.0.0.1:5000'
    
    routes_to_check = [
        ('/', 'GET', "Home Route"),
        ('/login', 'GET', "Login Page"),
        ('/register', 'GET', "Registration Page"),
        ('/logout', 'GET', "Logout Endpoint")
    ]
    
    print("🔍 Quick Route Verification")
    print("---------------------------")
    
    for path, method, description in routes_to_check:
        try:
            full_url = f'{BASE_URL}{path}'
            print(f"\n🔗 Checking {description}:")
            print(f"   URL: {full_url}")
            
            response = requests.get(full_url, timeout=5)
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Length: {len(response.text)} characters")
        
        except requests.RequestException as e:
            print(f"❌ Error accessing {path}: {e}")

if __name__ == '__main__':
    check_routes()
