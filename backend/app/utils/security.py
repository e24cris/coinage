from functools import wraps
from flask import request, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
import jwt
from datetime import datetime, timedelta

class SecurityMiddleware:
    """
    Comprehensive security middleware for Coinage application
    
    Features:
    - Rate Limiting
    - JWT Token Generation
    - Token Validation
    - IP-based Security
    """

    @staticmethod
    def rate_limiter(app):
        """
        Configure rate limiting for the application
        
        Limits:
        - Authentication routes: 5 requests per minute
        - Trading routes: 10 requests per minute
        - Payment routes: 3 requests per minute
        """
        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            default_limits=["100 per day", "30 per hour"]
        )

        # Authentication routes
        limiter.limit("5 per minute")(app.view_functions['auth.login'])
        limiter.limit("5 per minute")(app.view_functions['auth.register'])
        limiter.limit("3 per minute")(app.view_functions['auth.logout'])

        # Trading routes
        limiter.limit("10 per minute")(app.view_functions['trading.execute_trade'])
        limiter.limit("10 per minute")(app.view_functions['trading.get_trading_positions'])

        # Payment routes
        limiter.limit("3 per minute")(app.view_functions['payments.create_payment_request'])

        return limiter

    @staticmethod
    def generate_jwt_token(user, secret_key, expiration_hours=24):
        """
        Generate a JWT token for user authentication
        
        Args:
            user: User object
            secret_key: Application secret key
            expiration_hours: Token validity period
        
        Returns:
            JWT token string
        """
        payload = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(hours=expiration_hours),
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(payload, secret_key, algorithm='HS256')

    @staticmethod
    def validate_jwt_token(token, secret_key):
        """
        Validate JWT token
        
        Args:
            token: JWT token string
            secret_key: Application secret key
        
        Returns:
            Decoded token payload or None
        """
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def token_required(f):
        """
        Decorator to require JWT token for route access
        
        Validates:
        - Token presence
        - Token validity
        - Token expiration
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            # Check token in Authorization header
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]
            
            if not token:
                return jsonify({
                    'message': 'Authentication token is missing',
                    'error_code': 'AUTH_TOKEN_MISSING'
                }), 401
            
            # Validate token
            try:
                payload = SecurityMiddleware.validate_jwt_token(
                    token, 
                    current_app.config['SECRET_KEY']
                )
                
                if not payload:
                    return jsonify({
                        'message': 'Invalid or expired token',
                        'error_code': 'AUTH_TOKEN_INVALID'
                    }), 401
                
                # Optional: Additional checks like user existence
                
            except Exception as e:
                return jsonify({
                    'message': 'Token validation failed',
                    'error_code': 'AUTH_TOKEN_VALIDATION_ERROR'
                }), 500
            
            return f(*args, **kwargs)
        
        return decorated

    @staticmethod
    def log_security_event(event_type, details):
        """
        Log security-related events
        
        Args:
            event_type: Type of security event
            details: Event details dictionary
        """
        # In a real-world scenario, this would use a proper logging framework
        print(f"[SECURITY EVENT] {event_type}: {details}")
        # TODO: Implement secure logging to file/database
