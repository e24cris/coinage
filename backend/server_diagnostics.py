import os
import sys
import socket
import subprocess

def check_port_availability(port=5000):
    """
    Check if the specified port is available
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:
            print(f"❌ Port {port} is already in use!")
            return False
        else:
            print(f"✅ Port {port} is available.")
            return True
    except Exception as e:
        print(f"❌ Port check error: {e}")
        return False

def check_dependencies():
    """
    Verify required Python packages
    """
    print("\n📦 Dependency Check:")
    required_packages = [
        'flask', 'flask-sqlalchemy', 'flask-migrate', 
        'flask-login', 'flask-bcrypt', 'python-dotenv'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")

def check_environment_variables():
    """
    Verify critical environment variables
    """
    print("\n🔐 Environment Variables:")
    critical_vars = [
        'FLASK_APP', 'FLASK_ENV', 'DATABASE_URL', 
        'SECRET_KEY', 'DEBUG'
    ]
    
    for var in critical_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is NOT set")

def check_database_connection():
    """
    Attempt to establish database connection with comprehensive error handling
    """
    print("\n💾 Database Connection:")
    try:
        from app import create_app, db
        from sqlalchemy import inspect, text
        
        app = create_app()
        with app.app_context():
            # Attempt to connect and execute a simple query
            connection = db.engine.connect()
            result = connection.execute(text('SELECT 1'))
            result.close()
            connection.close()
            
            print("✅ Database connection successful")
            
            # Additional database health checks
            print("\n📊 Database Statistics:")
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"   Total Tables: {len(tables)}")
            print("   Tables:")
            for table in tables:
                print(f"   - {table}")
    
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("   Ensure all required packages are installed")
    
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()

def run_server_diagnostics():
    """
    Comprehensive server diagnostics
    """
    print("🔍 Coinage Application Server Diagnostics")
    print("---------------------------------------")
    
    # Run diagnostic checks
    check_port_availability()
    check_dependencies()
    check_environment_variables()
    check_database_connection()

def start_development_server():
    """
    Start Flask development server with comprehensive logging
    """
    print("\n🚀 Starting Development Server")
    print("-----------------------------")
    
    try:
        env = os.environ.copy()
        env['FLASK_APP'] = 'run.py'
        env['FLASK_ENV'] = 'development'
        env['FLASK_DEBUG'] = '1'
        
        subprocess.run(
            [sys.executable, '-m', 'flask', 'run'], 
            env=env, 
            cwd=os.path.dirname(os.path.abspath(__file__)),
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Server startup failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """
    Main entry point for server diagnostics and startup
    """
    run_server_diagnostics()
    
    # Prompt for server start
    start = input("\n❓ Would you like to start the development server? (y/n): ")
    if start.lower() == 'y':
        start_development_server()

if __name__ == '__main__':
    main()
