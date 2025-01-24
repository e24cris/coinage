import os
import sys
import subprocess
import time
import requests

def start_flask_server():
    """
    Start Flask development server in a separate process
    """
    print("🚀 Starting Flask Development Server...")
    env = os.environ.copy()
    env['FLASK_APP'] = 'run.py'
    env['FLASK_ENV'] = 'development'
    env['FLASK_DEBUG'] = '1'

    # Start Flask server as a subprocess
    server_process = subprocess.Popen(
        [sys.executable, '-m', 'flask', 'run'], 
        env=env, 
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    time.sleep(3)
    return server_process

def test_api_endpoints(base_url='http://127.0.0.1:5000'):
    """
    Test basic API endpoints with comprehensive error handling
    """
    print("🌐 API Endpoint Testing")
    print("----------------------")
    
    # List of endpoints to test
    endpoints = [
        ('/', 'GET', "Home Route"),
        ('/login', 'POST', "Login Endpoint"),
        ('/register', 'POST', "Registration Endpoint"),
        ('/logout', 'GET', "Logout Endpoint")
    ]
    
    for path, method, description in endpoints:
        try:
            full_url = f'{base_url}{path}'
            print(f"\n🔍 Testing {description}:")
            print(f"   URL: {full_url}")
            print(f"   Method: {method}")
            
            if method == 'GET':
                response = requests.get(full_url, timeout=5)
            else:
                response = requests.post(full_url, timeout=5)
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")  # Truncate long responses
            
        except requests.RequestException as e:
            print(f"❌ Error testing {path}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

def main():
    """
    Main function to start server and run tests
    """
    server_process = None
    try:
        # Start Flask server
        server_process = start_flask_server()
        
        # Run tests
        test_api_endpoints()
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
    finally:
        # Terminate server process if it exists
        if server_process:
            print("\n🛑 Stopping Flask Server...")
            server_process.terminate()
            server_process.wait()

if __name__ == '__main__':
    main()
