from app import create_app, db
from app.models.user import User
from datetime import datetime

def verify_admin_user():
    """
    Verify admin user details in the database
    """
    app = create_app()
    
    with app.app_context():
        # Find all admin users
        admin_users = User.query.filter_by(is_admin=True).all()
        
        if admin_users:
            print("🔐 Admin Users Verification:")
            for admin in admin_users:
                print(f"👤 Username: {admin.username}")
                print(f"📧 Email: {admin.email}")
                print(f"🕒 Registration Date: {admin.registration_date}")
                print(f"👑 Admin Status: {'Yes' if admin.is_admin else 'No'}")
                print(f"📅 Account Age: {(datetime.now() - admin.registration_date).days} days")
                print("---")
        else:
            print("❌ No admin users found in the database.")

if __name__ == '__main__':
    verify_admin_user()
