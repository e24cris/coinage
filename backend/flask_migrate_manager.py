import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init, migrate, upgrade

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_migrations(command='upgrade'):
    """
    Run database migrations with comprehensive error handling
    
    :param command: Migration command to run (init, migrate, upgrade)
    """
    try:
        # Import create_app and db
        from app import create_app, db

        # Create the Flask application
        app = create_app()

        # Initialize Flask-Migrate
        migrate_instance = Migrate(app, db)

        # Run migrations in application context
        with app.app_context():
            # Import models to ensure they are recognized by SQLAlchemy
            from app.models.user import User, TradingAccount, TradingPosition, Transaction, ManualPaymentRequest

            # Perform specific migration command
            if command == 'init':
                init()
                print("🎉 Migrations initialized successfully!")
            elif command == 'migrate':
                migrate(message="Automatic migration")
                print("🚀 Migration script created successfully!")
            elif command == 'upgrade':
                upgrade()
                print("✨ Database upgraded successfully!")
            else:
                print(f"❌ Unknown migration command: {command}")
                sys.exit(1)

    except Exception as e:
        print(f"❌ Migration error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    """
    Main entry point for migration management
    """
    # Check if a command is provided
    if len(sys.argv) < 2:
        print("Usage: python flask_migrate_manager.py [init|migrate|upgrade]")
        sys.exit(1)

    # Run the specified migration command
    command = sys.argv[1]
    run_migrations(command)

if __name__ == '__main__':
    main()
