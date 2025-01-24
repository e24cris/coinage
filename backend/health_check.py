import os
import sys
import socket
import requests

def check_server_health(url='http://127.0.0.1:5000'):
    """
    Comprehensive server health check
    """
    print("🩺 Coinage Application Health Check")
    print("----------------------------------")
    
    # Network Connectivity
    print("\n🌐 Network Connectivity:")
    try:
        socket.create_connection(("127.0.0.1", 5000), timeout=5)
        print("✅ Local server port is open")
    except (socket.error, socket.timeout):
        print("❌ Cannot connect to local server")
        return False
    
    # Server Endpoint Health
    print("\n🚦 Endpoint Health:")
    try:
        response = requests.get(url, timeout=5)
        print(f"✅ Root Endpoint Status: {response.status_code}")
        
        # Check response content
        if response.status_code == 200:
            print("\n📋 Response Details:")
            print(f"   Content Type: {response.headers.get('Content-Type', 'N/A')}")
            print(f"   Server: {response.headers.get('Server', 'N/A')}")
            
            # Try to parse JSON if possible
            try:
                json_response = response.json()
                print("   Response JSON:")
                for key, value in json_response.items():
                    print(f"   - {key}: {value}")
            except ValueError:
                print("   Response is not JSON")
        
    except requests.RequestException as e:
        print(f"❌ Server Health Check Failed: {e}")
        return False
    
    # Database Connection (via app)
    print("\n💾 Database Connection:")
    try:
        from app import create_app, db
        
        app = create_app()
        with app.app_context():
            # Simple database query
            result = db.session.execute('SELECT 1')
            result.close()
            print("✅ Database connection verified")
    
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    print("\n🎉 Overall System Health: GOOD")
    return True

def main():
    """
    Main entry point for health check
    """
    health_status = check_server_health()
    sys.exit(0 if health_status else 1)

if __name__ == '__main__':
    main()
