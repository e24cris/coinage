import os
from typing import Dict, Any
from dotenv import load_dotenv

class EnvironmentConfig:
    """
    Centralized environment configuration management
    
    Supports multiple environment types:
    - Development
    - Staging
    - Production
    - Testing
    """
    
    # Load environment variables
    load_dotenv()
    
    @classmethod
    def get_config(cls, env: str = None) -> Dict[str, Any]:
        """
        Retrieve configuration based on environment
        
        Args:
            env: Environment type (default: detected from FLASK_ENV)
        
        Returns:
            Dictionary of configuration settings
        """
        # Detect environment if not specified
        if not env:
            env = os.getenv('FLASK_ENV', 'development').lower()
        
        # Base configuration
        base_config = {
            # Database Configuration
            'DATABASE_URL': os.getenv('DATABASE_URL', 'sqlite:///default.db'),
            'DATABASE_POOL_SIZE': int(os.getenv('DATABASE_POOL_SIZE', 10)),
            
            # Security Settings
            'SECRET_KEY': os.getenv('SECRET_KEY', os.urandom(32)),
            'JWT_EXPIRATION_DELTA': int(os.getenv('JWT_EXPIRATION_DELTA', 3600)),
            
            # Logging Configuration
            'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
            'LOG_FILE': os.getenv('LOG_FILE', 'coinage.log'),
            
            # External Services
            'SENTRY_DSN': os.getenv('SENTRY_DSN', ''),
            'REDIS_URL': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        }
        
        # Environment-specific overrides
        env_configs = {
            'development': {
                **base_config,
                'DEBUG': True,
                'TESTING': False,
                'DATABASE_URL': 'sqlite:///dev.db',
                'LOG_LEVEL': 'DEBUG'
            },
            'staging': {
                **base_config,
                'DEBUG': False,
                'TESTING': False,
                'LOG_LEVEL': 'INFO'
            },
            'production': {
                **base_config,
                'DEBUG': False,
                'TESTING': False,
                'LOG_LEVEL': 'WARNING',
                'JWT_EXPIRATION_DELTA': 86400  # 24 hours
            },
            'testing': {
                **base_config,
                'DEBUG': True,
                'TESTING': True,
                'DATABASE_URL': 'sqlite:///:memory:',
                'LOG_LEVEL': 'ERROR'
            }
        }
        
        # Validate environment
        if env not in env_configs:
            raise ValueError(f"Invalid environment: {env}")
        
        return env_configs[env]
    
    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> None:
        """
        Validate configuration settings
        
        Args:
            config: Configuration dictionary to validate
        
        Raises:
            ValueError: If configuration is invalid
        """
        required_keys = [
            'DATABASE_URL', 
            'SECRET_KEY', 
            'LOG_LEVEL'
        ]
        
        for key in required_keys:
            if key not in config or not config[key]:
                raise ValueError(f"Missing required configuration: {key}")
        
        # Additional validation
        if not isinstance(config.get('DEBUG', False), bool):
            raise ValueError("DEBUG must be a boolean")
        
        if not isinstance(config.get('JWT_EXPIRATION_DELTA', 0), int):
            raise ValueError("JWT_EXPIRATION_DELTA must be an integer")
    
    @classmethod
    def load_environment(cls, env: str = None) -> Dict[str, Any]:
        """
        Load and validate environment configuration
        
        Args:
            env: Environment type
        
        Returns:
            Validated configuration dictionary
        """
        config = cls.get_config(env)
        cls.validate_config(config)
        return config

def main():
    """
    Demonstrate environment configuration loading
    """
    # Load development configuration
    dev_config = EnvironmentConfig.load_environment('development')
    print("Development Configuration:")
    for key, value in dev_config.items():
        print(f"{key}: {value}")
    
    # Load production configuration
    prod_config = EnvironmentConfig.load_environment('production')
    print("\nProduction Configuration:")
    for key, value in prod_config.items():
        print(f"{key}: {value}")

if __name__ == '__main__':
    main()
