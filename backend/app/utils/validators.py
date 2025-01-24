import re
import email_validator
from typing import Dict, Any, Tuple
import zxcvbn  # Password strength library

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class InputValidator:
    """Comprehensive input validation utility"""

    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """
        Validate username with comprehensive rules
        
        Rules:
        - 3-20 characters
        - Alphanumeric and underscore only
        - Cannot start with number
        """
        if not username:
            return False, "Username cannot be empty"
        
        if len(username) < 3 or len(username) > 20:
            return False, "Username must be 3-20 characters long"
        
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
            return False, "Username must start with a letter and contain only letters, numbers, and underscores"
        
        return True, ""

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email using email_validator library
        
        Checks:
        - Valid email format
        - Normalized email
        """
        try:
            # Validate and get normalized email
            valid = email_validator.validate_email(email)
            return True, valid.email
        except email_validator.EmailNotValidError as e:
            return False, str(e)

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password strength using zxcvbn
        
        Rules:
        - Minimum 8 characters
        - At least one uppercase, one lowercase, one number
        - Complexity score >= 3
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        # Check complexity
        result = zxcvbn.zxcvbn(password)
        
        if result['score'] < 3:
            return False, "Password is too weak. Use a more complex password."
        
        # Additional regex checks
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        return True, ""

    @staticmethod
    def validate_trade_request(trade_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate trading request parameters
        
        Checks:
        - Required fields present
        - Quantity is positive
        - Valid trade and account types
        """
        required_fields = ['symbol', 'quantity', 'trade_type', 'account_type']
        
        # Check all required fields are present
        for field in required_fields:
            if field not in trade_data:
                return False, f"Missing required field: {field}"
        
        # Validate quantity
        try:
            quantity = float(trade_data['quantity'])
            if quantity <= 0:
                return False, "Quantity must be a positive number"
        except ValueError:
            return False, "Invalid quantity"
        
        # Validate trade type
        valid_trade_types = ['buy', 'sell']
        if trade_data['trade_type'] not in valid_trade_types:
            return False, f"Invalid trade type. Must be one of {valid_trade_types}"
        
        # Validate account type
        valid_account_types = ['stock', 'forex', 'crypto']
        if trade_data['account_type'] not in valid_account_types:
            return False, f"Invalid account type. Must be one of {valid_account_types}"
        
        return True, ""

    @staticmethod
    def validate_payment_request(payment_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate payment request parameters
        
        Checks:
        - Amount is positive
        - Payment method is valid
        """
        # Check required fields
        if 'amount' not in payment_data:
            return False, "Missing amount"
        
        if 'payment_method' not in payment_data:
            return False, "Missing payment method"
        
        # Validate amount
        try:
            amount = float(payment_data['amount'])
            if amount <= 0:
                return False, "Payment amount must be positive"
            
            # Optional: Add max payment limit
            if amount > 100000:  # Configurable limit
                return False, "Payment amount exceeds maximum limit"
        except ValueError:
            return False, "Invalid payment amount"
        
        # Validate payment method
        valid_methods = ['bank_transfer', 'credit_card', 'crypto', 'paypal']
        if payment_data['payment_method'] not in valid_methods:
            return False, f"Invalid payment method. Must be one of {valid_methods}"
        
        return True, ""
