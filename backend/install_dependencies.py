import sys
import subprocess

def install_packages(packages):
    """Install multiple packages with detailed logging"""
    print("Starting dependency installation...")
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', package], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ Successfully installed {package}")
            else:
                print(f"❌ Failed to install {package}")
                print("Error output:", result.stderr)
        
        except Exception as e:
            print(f"❌ Error installing {package}: {e}")

def main():
    # Comprehensive list of required packages
    required_packages = [
        # Core Flask Packages
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-login',
        'flask-bcrypt',
        'flask-cors',
        'python-dotenv',
        
        # Database and ORM
        'SQLAlchemy',
        
        # Security
        'bcrypt',
        'email-validator',
        
        # Utilities
        'requests',
        'python-dateutil',
        'pytz',
        
        # Development and Testing
        'pytest',
        'coverage',
        'gunicorn'
    ]

    print("🚀 Coinage Backend Dependency Installer")
    print("--------------------------------------")
    
    install_packages(required_packages)
    
    print("\n🎉 Dependency installation complete!")
    print("Please verify the installation by running 'pip list'")

if __name__ == '__main__':
    main()
