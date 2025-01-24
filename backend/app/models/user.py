from app import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Boolean
from datetime import datetime
import enum

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class PaymentStatus(enum.Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    
    # Trading-related fields
    account_balance = Column(Float, default=0.0)
    registration_date = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)

    # Relationships
    trading_accounts = relationship('TradingAccount', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')
    payment_requests = relationship('ManualPaymentRequest', back_populates='user')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        base_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'account_balance': self.account_balance,
            'registration_date': self.registration_date.isoformat()
        }
        
        # Only include is_admin for admin users or when explicitly needed
        if hasattr(self, 'is_admin'):
            base_dict['is_admin'] = self.is_admin
        
        return base_dict

class TradingAccount(db.Model):
    __tablename__ = 'trading_accounts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    account_type = Column(String(50))  # e.g., 'stock', 'forex', 'crypto'
    balance = Column(Float, default=0.0)

    user = relationship('User', back_populates='trading_accounts')
    positions = relationship('TradingPosition', back_populates='trading_account')

class TradingPosition(db.Model):
    __tablename__ = 'trading_positions'

    id = Column(Integer, primary_key=True)
    trading_account_id = Column(Integer, db.ForeignKey('trading_accounts.id'), nullable=False)
    symbol = Column(String(20))
    quantity = Column(Float)
    entry_price = Column(Float)
    current_price = Column(Float)
    
    trading_account = relationship('TradingAccount', back_populates='positions')

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    amount = Column(Float)
    transaction_type = Column(String(50))  # deposit, withdrawal, trade
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='transactions')

class ManualPaymentRequest(db.Model):
    __tablename__ = 'manual_payment_requests'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    cryptocurrency = Column(String(50), nullable=False)  # e.g., 'BTC', 'ETH'
    wallet_address = Column(String(255), nullable=False)
    transaction_hash = Column(String(255))
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    proof_of_payment = Column(String(255))  # Path to uploaded payment proof
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    admin_notes = Column(String(500))

    user = relationship('User', back_populates='payment_requests')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'cryptocurrency': self.cryptocurrency,
            'wallet_address': self.wallet_address,
            'transaction_hash': self.transaction_hash,
            'status': self.status.value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'admin_notes': self.admin_notes
        }
