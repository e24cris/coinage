import os
from datetime import timedelta

class Config:
    """
    Comprehensive configuration for Coinage application
    """
    # Secret and Security Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///coinage.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Authentication Configuration
    AUTH_TOKEN_EXPIRATION = timedelta(hours=24)
    
    # Security Settings
    SECURITY_PASSWORD_SALT = os.environ.get('PASSWORD_SALT') or os.urandom(16)
    
    # Rate Limiting Configuration
    RATELIMIT_DEFAULT = "100 per day"
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    
    # Logging Configuration
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'false') == 'true'
    
    # Two-Factor Authentication
    TWO_FACTOR_ENABLED = os.environ.get('TWO_FACTOR_ENABLED', 'false') == 'true'
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Debug and Testing
    DEBUG = os.environ.get('FLASK_DEBUG', 'false') == 'true'
    TESTING = os.environ.get('FLASK_TESTING', 'false') == 'true'

class DevelopmentConfig(Config):
    """Configuration for development environment"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Configuration for production environment"""
    DEBUG = False
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    """Configuration for testing environment"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

def get_config():
    """
    Select configuration based on environment
    """
    env = os.environ.get('FLASK_ENV', 'development')
    config_selector = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    return config_selector.get(env, DevelopmentConfig)
