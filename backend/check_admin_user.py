from app import create_app, db
from app.models.user import User

def check_admin_users():
    """
    Check for existing admin users in the database
    """
    app = create_app()
    
    with app.app_context():
        # Find all admin users
        admin_users = User.query.filter_by(is_admin=True).all()
        
        if admin_users:
            print("🔐 Admin Users Found:")
            for admin in admin_users:
                print(f"👤 Username: {admin.username}")
                print(f"📧 Email: {admin.email}")
                print(f"🕒 Registration Date: {admin.registration_date}")
                print("---")
        else:
            print("❌ No admin users found in the database.")
            print("Consider creating an admin user using create_admin.py")

if __name__ == '__main__':
    check_admin_users()
