import os
import sys

# Ensure backend directory is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def initialize_database():
    """
    Comprehensive database initialization and verification
    """
    try:
        from app import create_app, db
        from app.models.user import User, TradingAccount, Transaction, ManualPaymentRequest
        from sqlalchemy import inspect

        # Create Flask application context
        app = create_app()

        with app.app_context():
            print("🚀 Database Initialization Process")
            print("--------------------------------")

            # Drop all existing tables (use with caution in production)
            print("\n🧹 Clearing Existing Database...")
            db.drop_all()

            # Create all database tables
            print("\n🏗️ Creating Database Tables...")
            db.create_all()

            # Verify table creation using SQLAlchemy inspector
            print("\n📊 Database Tables:")
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            # Verify specific tables
            required_tables = ['users', 'trading_accounts', 'transactions', 'manual_payment_requests']
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                print(f"\n❌ Missing Tables: {missing_tables}")
                return False
            
            for table in tables:
                print(f"   - {table}")

            # Create a default admin user
            print("\n👤 Creating Default Admin User...")
            admin_user = User(
                username='coinage_admin', 
                email='coinage_admin@coinage4.com', 
                is_admin=True
            )
            admin_user.set_password('admin_password')
            
            db.session.add(admin_user)
            db.session.commit()

            print(f"\n✅ Database Initialization Complete!")
            print(f"   Total Tables Created: {len(tables)}")
            print(f"   Admin User Created: coinage_admin")

    except Exception as e:
        print(f"❌ Database Initialization Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """
    Main entry point for database initialization
    """
    result = initialize_database()
    sys.exit(0 if result else 1)

if __name__ == '__main__':
    main()
