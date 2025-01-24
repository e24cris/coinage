from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.utils.validators import InputValidator, ValidationError
from app.utils.security import SecurityMiddleware
from app.utils.error_handler import ErrorHandler
from app.utils.auth_strategy import AuthenticationStrategy
import logging

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Enhanced user registration with comprehensive validation
    """
    try:
        # Validate JSON input
        if not request.is_json:
            raise ValidationError("Request must be JSON", "INVALID_REQUEST")
        
        data = request.get_json()
        
        # Validate username
        username_valid, username_error = InputValidator.validate_username(data.get('username', ''))
        if not username_valid:
            raise ValidationError(username_error, "INVALID_USERNAME")
        
        # Validate email
        email_valid, email_result = InputValidator.validate_email(data.get('email', ''))
        if not email_valid:
            raise ValidationError(email_result, "INVALID_EMAIL")
        
        # Validate password
        password_valid, password_error = InputValidator.validate_password(data.get('password', ''))
        if not password_valid:
            raise ValidationError(password_error, "WEAK_PASSWORD")
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            raise ValidationError("Username already exists", "USERNAME_EXISTS")
        
        if User.query.filter_by(email=data['email']).first():
            raise ValidationError("Email already exists", "EMAIL_EXISTS")
        
        # Create new user with secure password hashing
        new_user = User(
            username=data['username'], 
            email=data['email']
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        # Log security event
        SecurityMiddleware.log_security_event('USER_REGISTRATION', {
            'username': new_user.username,
            'email': new_user.email
        })
        
        return jsonify({
            'message': 'Registration successful', 
            'user': new_user.to_dict()
        }), 201

    except ValidationError as ve:
        return ErrorHandler.handle_error(ve, ve.error_code, 400)
    except Exception as e:
        return ErrorHandler.handle_error(e, 'REGISTRATION_ERROR', 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Enhanced user login with security checks
    """
    try:
        # Validate JSON input
        if not request.is_json:
            raise ValidationError("Request must be JSON", "INVALID_REQUEST")
        
        data = request.get_json()
        
        # Validate username and password presence
        if not all(key in data for key in ['username', 'password']):
            raise ValidationError("Missing username or password", "MISSING_CREDENTIALS")
        
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            # Successful login
            login_user(user)
            
            # Generate JWT token
            token = SecurityMiddleware.generate_jwt_token(
                user, 
                current_app.config['SECRET_KEY']
            )
            
            # Log login event
            SecurityMiddleware.log_security_event('USER_LOGIN', {
                'username': user.username
            })
            
            return jsonify({
                'message': 'Login successful', 
                'user': user.to_dict(),
                'token': token
            }), 200
        
        # Failed login
        raise ValidationError("Invalid credentials", "INVALID_CREDENTIALS")

    except ValidationError as ve:
        return ErrorHandler.handle_error(ve, ve.error_code, 401)
    except Exception as e:
        return ErrorHandler.handle_error(e, 'LOGIN_ERROR', 500)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Enhanced user logout with security logging
    """
    try:
        # Log logout event
        SecurityMiddleware.log_security_event('USER_LOGOUT', {
            'username': current_user.username
        })
        
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200

    except Exception as e:
        return ErrorHandler.handle_error(e, 'LOGOUT_ERROR', 500)

@auth_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """
    Retrieve user profile with enhanced security
    """
    try:
        # Log profile access
        SecurityMiddleware.log_security_event('PROFILE_ACCESS', {
            'username': current_user.username
        })
        
        return jsonify(current_user.to_dict()), 200

    except Exception as e:
        return ErrorHandler.handle_error(e, 'PROFILE_ERROR', 500)
