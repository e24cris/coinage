import os
from datetime import timedelta

# Determine the base directory of the project
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Config:
    # Base Directory
    BASE_DIR = BASE_DIR

    # Security Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(BASE_DIR, "coinage.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # API Keys (should be set in environment)
    FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY')
    ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')
    
    # Payment Gateway Keys
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    COINBASE_API_KEY = os.environ.get('COINBASE_API_KEY')
    
    # Manual Payment Configuration
    PAYMENT_PROOF_UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'payment_proofs')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file upload
    
    # Logging Configuration
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'false') == 'true'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
