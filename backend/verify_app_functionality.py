import sys
import os
from flask import Flask
from sqlalchemy import inspect

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_application_functionality():
    """
    Comprehensive application functionality verification
    """
    print("🔍 Coinage Application Functionality Verification")
    print("-----------------------------------------------")

    try:
        # Import application components
        from app import create_app, db
        from app.models.user import User, TradingAccount, ManualPaymentRequest

        # Create application context
        app = create_app()

        with app.app_context():
            # Database Connection Check
            print("📦 Database Connection:")
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"   Connected Tables: {tables}")

            # User Model Verification
            print("\n👥 User Model:")
            admin_count = User.query.filter_by(is_admin=True).count()
            total_users = User.query.count()
            print(f"   Total Users: {total_users}")
            print(f"   Admin Users: {admin_count}")

            # Trading Account Verification
            print("\n💼 Trading Accounts:")
            trading_accounts = TradingAccount.query.count()
            print(f"   Total Trading Accounts: {trading_accounts}")

            # Payment Request Verification
            print("\n💰 Payment Requests:")
            payment_requests = ManualPaymentRequest.query.count()
            print(f"   Total Payment Requests: {payment_requests}")

            # Configuration Checks
            print("\n⚙️ Application Configuration:")
            print(f"   Debug Mode: {app.debug}")
            print(f"   Testing: {app.testing}")
            print(f"   Environment: {app.env}")

    except Exception as e:
        print(f"❌ Verification Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    verify_application_functionality()
