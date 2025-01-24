import os
import sys
import inspect

def diagnose_routes():
    """
    Comprehensive route and endpoint diagnosis
    """
    print("🔍 Route and Endpoint Diagnostic Tool")
    print("-------------------------------------")

    try:
        # Import the Flask app
        from app import create_app
        app = create_app()

        print("\n🗺️ Registered Routes:")
        for rule in app.url_map.iter_rules():
            print(f"   🔗 {rule.endpoint}")
            print(f"      Path: {rule}")
            print(f"      Methods: {list(rule.methods)}")
            print("---")

    except ImportError as e:
        print(f"❌ Import Error: {e}")
    except Exception as e:
        print(f"❌ Diagnostic Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """
    Main entry point for route diagnostics
    """
    diagnose_routes()

if __name__ == '__main__':
    main()
