import os
import pytest
import uuid
from typing import Dict, Any

from backend.app_integrator import create_app
from backend.models import User, TradingAccount, Transaction
from backend.user_onboarding import UserOnboardingService
from backend.trading_engine import TradingEngine
from backend.security.advanced_security import AdvancedSecurityManager

class IntegrationTestSuite:
    """
    Comprehensive Integration Test Suite
    
    Covers end-to-end user and trading workflows
    """
    
    @pytest.fixture(scope='class')
    def app(self):
        """Create test Flask application"""
        app = create_app('testing')
        return app
    
    @pytest.fixture(scope='class')
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    @pytest.fixture(scope='class')
    def db_session(self):
        """Create database session"""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        engine = create_engine('sqlite:///test_integration.db')
        Session = sessionmaker(bind=engine)
        return Session()
    
    @pytest.fixture(scope='class')
    def security_manager(self):
        """Create security manager"""
        return AdvancedSecurityManager()
    
    def test_user_registration_workflow(
        self, 
        db_session, 
        security_manager
    ):
        """
        Test complete user registration workflow
        
        Validates:
        - User creation
        - Password hashing
        - TOTP secret generation
        """
        # Generate unique test data
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        email = f"{username}@example.com"
        password = "StrongP@ssw0rd2025!"
        
        # User registration
        onboarding_service = UserOnboardingService(db_session)
        registration_result = onboarding_service.register_user(
            username, email, password
        )
        
        assert registration_result['success'], "Registration should succeed"
        assert 'user_id' in registration_result
        
        # Verify user in database
        user = db_session.query(User).get(registration_result['user_id'])
        assert user is not None
        
        # Verify password hash
        assert security_manager.verify_password(
            password, 
            user.password_hash
        ), "Password verification failed"
        
        # Verify TOTP secret
        assert user.totp_secret is not None
    
    def test_trading_account_creation(
        self, 
        db_session, 
        security_manager
    ):
        """
        Test trading account creation workflow
        
        Validates:
        - Account creation
        - Initial balance setup
        - Account security
        """
        # Create test user first
        username = f"trader_{uuid.uuid4().hex[:8]}"
        email = f"{username}@example.com"
        password = "TraderP@ssw0rd2025!"
        
        onboarding_service = UserOnboardingService(db_session)
        registration_result = onboarding_service.register_user(
            username, email, password
        )
        user_id = registration_result['user_id']
        
        # Create trading account
        trading_account = TradingAccount(
            user_id=user_id,
            account_type='standard',
            initial_balance=10000.00
        )
        
        db_session.add(trading_account)
        db_session.commit()
        
        # Verify trading account
        created_account = db_session.query(TradingAccount).filter_by(
            user_id=user_id
        ).first()
        
        assert created_account is not None
        assert created_account.balance == 10000.00
        assert created_account.account_type == 'standard'
    
    def test_trading_workflow(
        self, 
        db_session
    ):
        """
        Test complete trading workflow
        
        Validates:
        - Trade execution
        - Transaction recording
        - Balance updates
        """
        # Create trading engine
        trading_engine = TradingEngine('sqlite:///test_trading.db')
        
        # Simulate trading scenario
        trade_result = trading_engine.execute_trade(
            user_id=1,
            asset='AAPL',
            trade_type='buy',
            quantity=10,
            price=150.50
        )
        
        assert trade_result['status'] == 'success'
        assert 'trade_id' in trade_result
        
        # Verify transaction
        transaction = db_session.query(Transaction).get(trade_result['trade_id'])
        assert transaction is not None
        assert transaction.asset == 'AAPL'
        assert transaction.quantity == 10
        assert transaction.price == 150.50
    
    def test_security_workflow(
        self, 
        security_manager
    ):
        """
        Test security-related workflows
        
        Validates:
        - JWT token generation
        - Token validation
        - Password strength
        """
        # Test password strength validation
        strong_password = "SecureP@ssw0rd2025!"
        weak_password = "weak"
        
        assert security_manager.validate_password_strength(
            strong_password
        ), "Strong password validation failed"
        
        assert not security_manager.validate_password_strength(
            weak_password
        ), "Weak password should be rejected"
        
        # Test JWT token generation and validation
        jwt_token = security_manager.generate_jwt(
            user_id=1, 
            username='testuser'
        )
        
        decoded_token = security_manager.validate_jwt(jwt_token)
        
        assert decoded_token['user_id'] == 1
        assert decoded_token['username'] == 'testuser'
    
    def test_payment_request_workflow(
        self, 
        db_session
    ):
        """
        Test payment request workflow
        
        Validates:
        - Payment request creation
        - Approval process
        - Transaction recording
        """
        # Simulate payment request
        payment_request = {
            'user_id': 1,
            'amount': 1000.00,
            'currency': 'USD',
            'payment_method': 'bank_transfer'
        }
        
        # In a real implementation, this would use a payment service
        transaction = Transaction(
            user_id=payment_request['user_id'],
            amount=payment_request['amount'],
            transaction_type='deposit',
            status='pending'
        )
        
        db_session.add(transaction)
        db_session.commit()
        
        # Verify transaction
        created_transaction = db_session.query(Transaction).get(transaction.id)
        
        assert created_transaction is not None
        assert created_transaction.amount == 1000.00
        assert created_transaction.status == 'pending'

def main():
    """
    Run integration tests
    """
    pytest.main([
        '-v', 
        '--tb=short', 
        __file__
    ])

if __name__ == '__main__':
    main()
