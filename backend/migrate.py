import os
import sys
import shutil
import traceback
import importlib.util
import subprocess
import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def install_package(package):
    """Install a single package"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")
        return False
    return True

def check_and_install_dependencies():
    """Comprehensive dependency checking and installation"""
    # List of required packages
    required_packages = [
        'flask', 
        'flask-sqlalchemy', 
        'flask-migrate', 
        'flask-login', 
        'flask-bcrypt', 
        'flask-cors',
        'python-dotenv'
    ]

    # Track missing packages
    missing_packages = []

    # Check each package
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Missing package: {package}")
            missing_packages.append(package)

    # Install missing packages
    if missing_packages:
        print(f"Installing missing packages: {missing_packages}")
        for package in missing_packages:
            if not install_package(package):
                print(f"Critical: Unable to install {package}")
                sys.exit(1)

def check_module_exists(module_name):
    """
    Check if a module exists and can be imported
    
    Args:
        module_name (str): Full module path to check
    
    Returns:
        bool: True if module exists and can be imported, False otherwise
    """
    try:
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except ImportError:
        return False

def diagnose_import_error(module_name):
    """
    Provide detailed diagnosis for import errors
    
    Args:
        module_name (str): Full module path that failed to import
    """
    print(f"\n🔍 Diagnosing import error for: {module_name}")
    
    # Check directory structure
    base_path = os.path.join(os.path.dirname(__file__), 'app')
    print(f"Checking directory: {base_path}")
    
    # List all subdirectories and files
    for root, dirs, files in os.walk(base_path):
        relative_path = os.path.relpath(root, base_path)
        print(f"\nDirectory: {relative_path}")
        print("Subdirectories:", dirs)
        print("Files:", files)
    
    # Detailed path checks
    module_parts = module_name.split('.')
    current_path = base_path
    for part in module_parts[1:]:
        current_path = os.path.join(current_path, part)
        print(f"\nChecking path: {current_path}")
        if os.path.exists(current_path + '.py'):
            print(f"✅ Found module file: {part}.py")
        elif os.path.exists(current_path) and os.path.isdir(current_path):
            print(f"✅ Found directory: {part}")
        else:
            print(f"❌ Module/Directory not found: {part}")

def reset_migrations():
    """
    Reset migrations directory if it exists and is not empty
    """
    migrations_path = os.path.join(os.path.dirname(__file__), 'migrations')
    
    if os.path.exists(migrations_path) and os.listdir(migrations_path):
        print("🔄 Existing migrations directory found. Resetting...")
        
        # Backup existing migrations
        backup_path = migrations_path + '_backup_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        shutil.move(migrations_path, backup_path)
        print(f"📦 Existing migrations backed up to: {backup_path}")
        
        # Recreate empty migrations directory
        os.makedirs(migrations_path)
        print("✨ Migrations directory reset successfully.")

def run_migrations():
    """Run database migrations with comprehensive error handling"""
    try:
        # Reset migrations if needed
        reset_migrations()

        # Dynamically check and import app module
        if not check_module_exists('app'):
            print("❌ 'app' module not found. Checking project structure...")
            diagnose_import_error('app')
            sys.exit(1)

        # Import create_app and db
        from app import create_app, db
        from flask_migrate import Migrate, init, migrate, upgrade

        app = create_app()

        with app.app_context():
            # Initialize Migrate
            migrate_instance = Migrate(app, db)

            # Perform migration steps
            try:
                # Initialize migrations if not already done
                init()

                # Create a new migration
                migrate(message="Initial migration")

                # Apply migrations
                upgrade()

                print("🎉 Migrations completed successfully!")
            except Exception as e:
                print(f"❌ Migration error: {e}")
                traceback.print_exc()
                sys.exit(1)

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nDetailed Troubleshooting:")
        print("1. Ensure all dependencies are installed")
        print("2. Check your virtual environment")
        print("3. Verify Python path is correct")
        
        # Diagnose specific import error
        module_name = str(e).split("'")[1]
        diagnose_import_error(module_name)
        
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    check_and_install_dependencies()
    run_migrations()
