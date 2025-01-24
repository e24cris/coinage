import sys
import os

def diagnose_python_path():
    """
    Comprehensive Python path and import diagnostics
    """
    print("🔍 Python Path Diagnostics")
    print("-------------------------")
    
    # Print Python executable and version
    print(f"\n🐍 Python Executable: {sys.executable}")
    print(f"Python Version: {sys.version}")
    
    # Print current working directory
    print(f"\n📁 Current Working Directory: {os.getcwd()}")
    
    # Print Python path
    print("\n🗂️ Python Path:")
    for path in sys.path:
        print(f"   - {path}")
    
    # Test importing key libraries
    libraries_to_test = [
        'flask', 
        'sqlalchemy', 
        'flask_login', 
        'flask_sqlalchemy', 
        'flask_bcrypt'
    ]
    
    print("\n📦 Library Import Test:")
    for lib in libraries_to_test:
        try:
            __import__(lib)
            print(f"   ✅ Successfully imported: {lib}")
        except ImportError as e:
            print(f"   ❌ Failed to import {lib}: {e}")

def main():
    """
    Main entry point for import diagnostics
    """
    diagnose_python_path()

if __name__ == '__main__':
    main()
