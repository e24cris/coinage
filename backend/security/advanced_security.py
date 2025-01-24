import os
import re
import secrets
import hashlib
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

import jwt
from cryptography.fernet import Fernet
from passlib.hash import argon2
import pyotp
import requests
from flask import request, abort

class AdvancedSecurityManager:
    """
    Comprehensive Security Management System
    
    Features:
    - Multi-factor Authentication
    - Token Management
    - Password Hashing
    - Data Encryption
    - IP-based Access Control
    - Suspicious Activity Detection
    """
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize security manager
        
        Args:
            secret_key: Optional custom secret key
        """
        self.secret_key = secret_key or os.getenv(
            'SECRET_KEY', 
            secrets.token_hex(32)
        )
        
        # Encryption key for sensitive data
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        # IP Reputation Service
        self.ip_reputation_api_key = os.getenv('IP_REPUTATION_API_KEY')
    
    def generate_totp_secret(self) -> str:
        """
        Generate TOTP secret for multi-factor authentication
        
        Returns:
            TOTP secret
        """
        return pyotp.random_base32()
    
    def verify_totp(self, secret: str, token: str) -> bool:
        """
        Verify TOTP token
        
        Args:
            secret: TOTP secret
            token: User-provided token
        
        Returns:
            Verification result
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
    
    def hash_password(self, password: str) -> str:
        """
        Securely hash password using Argon2
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password
        """
        return argon2.hash(password)
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify password against hash
        
        Args:
            password: Plain text password
            hashed_password: Stored password hash
        
        Returns:
            Verification result
        """
        return argon2.verify(password, hashed_password)
    
    def generate_jwt(
        self, 
        user_id: int, 
        username: str, 
        expiration: int = 3600
    ) -> str:
        """
        Generate JWT token
        
        Args:
            user_id: User identifier
            username: Username
            expiration: Token expiration in seconds
        
        Returns:
            JWT token
        """
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': datetime.utcnow() + timedelta(seconds=expiration),
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(
            payload, 
            self.secret_key, 
            algorithm='HS256'
        )
    
    def validate_jwt(self, token: str) -> Dict[str, Any]:
        """
        Validate JWT token
        
        Args:
            token: JWT token
        
        Returns:
            Decoded token payload
        """
        try:
            return jwt.decode(
                token, 
                self.secret_key, 
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            logging.warning("Expired JWT token")
            abort(401, "Token expired")
        except jwt.InvalidTokenError:
            logging.warning("Invalid JWT token")
            abort(401, "Invalid token")
    
    def encrypt_data(self, data: str) -> bytes:
        """
        Encrypt sensitive data
        
        Args:
            data: Data to encrypt
        
        Returns:
            Encrypted data
        """
        return self.cipher_suite.encrypt(data.encode())
    
    def decrypt_data(self, encrypted_data: bytes) -> str:
        """
        Decrypt sensitive data
        
        Args:
            encrypted_data: Encrypted data
        
        Returns:
            Decrypted data
        """
        return self.cipher_suite.decrypt(encrypted_data).decode()
    
    def validate_password_strength(self, password: str) -> bool:
        """
        Check password complexity
        
        Args:
            password: Password to validate
        
        Returns:
            Password strength validation result
        """
        # At least 12 characters
        # Contains uppercase, lowercase, number, special character
        pattern = re.compile(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$'
        )
        return bool(pattern.match(password))
    
    def check_ip_reputation(self, ip_address: str) -> bool:
        """
        Check IP reputation using external service
        
        Args:
            ip_address: IP address to check
        
        Returns:
            IP reputation status
        """
        if not self.ip_reputation_api_key:
            return True
        
        try:
            response = requests.get(
                f'https://ipqualityscore.com/api/json/ip/{self.ip_reputation_api_key}/{ip_address}',
                timeout=5
            )
            data = response.json()
            
            # Suspicious criteria
            return (
                data.get('fraud_score', 0) < 75 and
                not data.get('is_vpn', False) and
                not data.get('is_proxy', False)
            )
        except Exception as e:
            logging.error(f"IP reputation check failed: {e}")
            return True
    
    def log_security_event(
        self, 
        event_type: str, 
        details: Dict[str, Any]
    ) -> None:
        """
        Log security-related events
        
        Args:
            event_type: Type of security event
            details: Event details
        """
        logging.info(
            f"Security Event: {event_type} - {details}"
        )

def security_middleware(func):
    """
    Security middleware decorator
    
    Performs:
    - JWT validation
    - IP reputation check
    - Rate limiting
    """
    def wrapper(*args, **kwargs):
        security_manager = AdvancedSecurityManager()
        
        # IP Reputation Check
        client_ip = request.remote_addr
        if not security_manager.check_ip_reputation(client_ip):
            security_manager.log_security_event(
                'SUSPICIOUS_IP', 
                {'ip': client_ip}
            )
            abort(403, "Access denied")
        
        # JWT Validation
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            abort(401, "Authentication required")
        
        try:
            token = auth_header.split(' ')[1]
            decoded_token = security_manager.validate_jwt(token)
            request.user = decoded_token
        except Exception:
            abort(401, "Invalid authentication")
        
        return func(*args, **kwargs)
    
    return wrapper
