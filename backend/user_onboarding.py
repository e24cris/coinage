import os
import logging
from typing import Dict, Any, Optional
from flask import current_app
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError

from backend.models import User
from backend.security.advanced_security import AdvancedSecurityManager
from backend.notifications.email_service import EmailService

class UserOnboardingService:
    """
    Comprehensive User Onboarding Service
    
    Handles:
    - User Registration
    - Email Verification
    - Profile Completion
    - Welcome Workflows
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize onboarding service
        
        Args:
            db_session: Database session
        """
        self.db_session = db_session
        self.security_manager = AdvancedSecurityManager()
        self.email_service = EmailService()
    
    def validate_registration_data(
        self, 
        username: str, 
        email: str, 
        password: str
    ) -> Dict[str, str]:
        """
        Validate user registration data
        
        Args:
            username: Desired username
            email: User email
            password: User password
        
        Returns:
            Validation errors or empty dict
        """
        errors = {}
        
        # Username validation
        if not username or len(username) < 3:
            errors['username'] = 'Username must be at least 3 characters'
        
        # Email validation
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            errors['email'] = str(e)
        
        # Password strength validation
        if not self.security_manager.validate_password_strength(password):
            errors['password'] = (
                'Password must be at least 12 characters, '
                'include uppercase, lowercase, number, and special character'
            )
        
        return errors
    
    def register_user(
        self, 
        username: str, 
        email: str, 
        password: str
    ) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            username: Desired username
            email: User email
            password: User password
        
        Returns:
            Registration result
        """
        # Validate registration data
        validation_errors = self.validate_registration_data(
            username, email, password
        )
        
        if validation_errors:
            return {
                'success': False,
                'errors': validation_errors
            }
        
        # Check if user already exists
        existing_user = self.db_session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            return {
                'success': False,
                'errors': {
                    'username': 'Username or email already exists'
                }
            }
        
        # Generate TOTP secret for 2FA
        totp_secret = self.security_manager.generate_totp_secret()
        
        # Hash password
        hashed_password = self.security_manager.hash_password(password)
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            totp_secret=totp_secret,
            is_verified=False
        )
        
        try:
            self.db_session.add(new_user)
            self.db_session.commit()
            
            # Send welcome email
            self.send_welcome_email(new_user)
            
            return {
                'success': True,
                'user_id': new_user.id,
                'totp_secret': totp_secret
            }
        
        except Exception as e:
            self.db_session.rollback()
            logging.error(f"User registration failed: {e}")
            
            return {
                'success': False,
                'errors': {
                    'registration': 'An unexpected error occurred'
                }
            }
    
    def send_welcome_email(self, user: User) -> None:
        """
        Send welcome email to new user
        
        Args:
            user: Newly registered user
        """
        verification_link = self.generate_verification_link(user)
        
        email_template = f"""
        Welcome to Coinage, {user.username}!

        Please verify your email by clicking the link below:
        {verification_link}

        Your 2FA secret is: {user.totp_secret}
        Please set up two-factor authentication in your account settings.

        Best regards,
        Coinage Team
        """
        
        self.email_service.send_email(
            to_email=user.email,
            subject='Welcome to Coinage - Verify Your Email',
            body=email_template
        )
    
    def generate_verification_link(self, user: User) -> str:
        """
        Generate email verification link
        
        Args:
            user: User to generate link for
        
        Returns:
            Verification link
        """
        base_url = current_app.config.get(
            'EMAIL_VERIFICATION_URL', 
            'https://coinage.com/verify'
        )
        
        verification_token = self.security_manager.generate_jwt(
            user_id=user.id,
            username=user.username,
            expiration=3600  # 1 hour
        )
        
        return f"{base_url}?token={verification_token}"
    
    def verify_email(self, token: str) -> Dict[str, Any]:
        """
        Verify user email using JWT token
        
        Args:
            token: Verification JWT token
        
        Returns:
            Verification result
        """
        try:
            decoded_token = self.security_manager.validate_jwt(token)
            user_id = decoded_token['user_id']
            
            user = self.db_session.query(User).get(user_id)
            
            if not user:
                return {
                    'success': False,
                    'message': 'User not found'
                }
            
            user.is_verified = True
            self.db_session.commit()
            
            return {
                'success': True,
                'message': 'Email verified successfully'
            }
        
        except Exception as e:
            logging.error(f"Email verification failed: {e}")
            return {
                'success': False,
                'message': 'Invalid or expired verification token'
            }
    
    def complete_profile(
        self, 
        user_id: int, 
        profile_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Complete user profile after registration
        
        Args:
            user_id: User ID
            profile_data: Additional profile information
        
        Returns:
            Profile completion result
        """
        user = self.db_session.query(User).get(user_id)
        
        if not user:
            return {
                'success': False,
                'message': 'User not found'
            }
        
        try:
            # Update user profile
            user.first_name = profile_data.get('first_name')
            user.last_name = profile_data.get('last_name')
            user.country = profile_data.get('country')
            user.phone_number = profile_data.get('phone_number')
            
            self.db_session.commit()
            
            return {
                'success': True,
                'message': 'Profile completed successfully'
            }
        
        except Exception as e:
            self.db_session.rollback()
            logging.error(f"Profile completion failed: {e}")
            
            return {
                'success': False,
                'message': 'Profile completion failed'
            }

def main():
    """
    Example usage of user onboarding service
    """
    # Simulated database session
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine('sqlite:///coinage.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    onboarding_service = UserOnboardingService(session)
    
    # Example registration
    registration_result = onboarding_service.register_user(
        username='johndoe',
        email='john@example.com',
        password='StrongP@ssw0rd!'
    )
    
    print("Registration Result:", registration_result)

if __name__ == '__main__':
    main()
