import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def validate_input(username, email, password):
    """
    Validate input parameters for admin user creation
    """
    errors = []
    
    # Username validation
    if not username or len(username) < 3:
        errors.append("Username must be at least 3 characters long")
    
    # Email validation
    if not email or '@' not in email:
        errors.append("Invalid email address")
    
    # Password validation
    if not password or len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    return errors

def create_admin_user(username, email, password):
    """
    Create an admin user with comprehensive error handling
    """
    # Validate input first
    input_errors = validate_input(username, email, password)
    if input_errors:
        print(" Admin User Creation Failed:")
        for error in input_errors:
            print(f"   - {error}")
        sys.exit(1)

    try:
        from app import create_app, db
        from app.models.user import User

        app = create_app()
        
        with app.app_context():
            # Check if admin already exists
            existing_admin = User.query.filter_by(username=username).first()
            if existing_admin:
                print(f" Admin user {username} already exists.")
                sys.exit(1)

            # Create new admin user
            admin_user = User(
                username=username, 
                email=email,
                is_admin=True,
                first_name='Admin',
                last_name='User'
            )
            admin_user.set_password(password)
            
            db.session.add(admin_user)
            db.session.commit()
            
            print(f" Admin user {username} created successfully!")
            print(f"   Email: {email}")
            print("   Role: System Administrator")

    except Exception as e:
        print(f" Error creating admin user: {e}")
        sys.exit(1)

def main():
    """
    Main entry point for admin user creation
    """
    # Check if correct number of arguments is provided
    if len(sys.argv) != 4:
        print(" Incorrect usage!")
        print("Usage: python create_admin.py <username> <email> <password>")
        print("\nExample:")
        print("   python create_admin.py coinage_admin coinage_admin@example.com StrongAdminPassword123!")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    create_admin_user(username, email, password)

if __name__ == '__main__':
    main()
