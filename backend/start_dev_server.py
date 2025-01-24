import os
import subprocess
import sys

def start_development_server():
    """
    Start Flask development server with comprehensive environment setup
    """
    try:
        # Set environment variables
        env = os.environ.copy()
        env['FLASK_APP'] = 'run.py'
        env['FLASK_ENV'] = 'development'
        env['FLASK_DEBUG'] = '1'

        print("🚀 Starting Coinage Development Server...")
        print("-----------------------------------")
        print("🔧 Configuration:")
        print(f"   FLASK_APP: {env['FLASK_APP']}")
        print(f"   FLASK_ENV: {env['FLASK_ENV']}")
        print(f"   FLASK_DEBUG: {env['FLASK_DEBUG']}")
        print("-----------------------------------")

        # Run Flask development server
        subprocess.run([sys.executable, '-m', 'flask', 'run'], 
                       env=env, 
                       cwd=os.path.dirname(os.path.abspath(__file__)),
                       check=True)

    except subprocess.CalledProcessError as e:
        print(f"❌ Server startup failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == '__main__':
    start_development_server()
