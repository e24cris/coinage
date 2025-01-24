import os
import sys
import traceback

# Ensure backend directory is in Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def debug_import_path():
    """
    Comprehensive import path debugging
    """
    print("🔍 Import Path Diagnostics")
    print("-------------------------")
    
    # Print Python path
    print("\n🗂️ Python Path:")
    for path in sys.path:
        print(f"   - {path}")
    
    # Print current working directory
    print(f"\n📁 Current Working Directory: {os.getcwd()}")

def debug_routes():
    """
    Comprehensive route and application debugging
    """
    debug_import_path()

    try:
        # Attempt to import with detailed tracing
        print("\n🔬 Importing Application Components")
        
        # Detailed import tracing
        try:
            import app
            print("✅ Successfully imported app module")
        except ImportError as e:
            print(f"❌ Failed to import app module: {e}")
            print("Import Traceback:")
            traceback.print_exc()
            return

        try:
            from app import create_app, db
            print("✅ Successfully imported create_app and db")
        except ImportError as e:
            print(f"❌ Failed to import create_app or db: {e}")
            print("Import Traceback:")
            traceback.print_exc()
            return

        try:
            from flask import request, jsonify
            from app.models.user import User
            from flask_login import login_user, logout_user, login_required, current_user
            print("✅ Successfully imported all required modules")
        except ImportError as e:
            print(f"❌ Failed to import some modules: {e}")
            print("Import Traceback:")
            traceback.print_exc()
            return

        # Create Flask application context
        app = create_app()

        # Capture and print all routes
        print("\n🗺️ Registered Routes:")
        for rule in app.url_map.iter_rules():
            print(f"   🔗 {rule.endpoint}")
            print(f"      Path: {rule}")
            print(f"      Methods: {list(rule.methods)}")
            print("---")

        # Test route handlers
        with app.test_client() as client:
            # Registration Test
            print("\n🆕 Registration Route Test:")
            reg_response = client.post('/auth/register', json={
                'username': 'test_debug_user',
                'email': 'debug@coinage.com',
                'password': 'debug_password'
            })
            print(f"   Status Code: {reg_response.status_code}")
            print(f"   Response Data: {reg_response.get_json()}")

            # Login Test
            print("\n🔑 Login Route Test:")
            login_response = client.post('/auth/login', json={
                'username': 'test_debug_user',
                'password': 'debug_password'
            })
            print(f"   Status Code: {login_response.status_code}")
            print(f"   Response Data: {login_response.get_json()}")

    except Exception as e:
        print(f"❌ Debugging Error: {e}")
        traceback.print_exc()

def main():
    """
    Main entry point for route debugging
    """
    debug_routes()

if __name__ == '__main__':
    main()
