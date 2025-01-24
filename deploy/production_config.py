import os
from typing import Dict, Any

class ProductionConfig:
    """
    Comprehensive Production Configuration Management
    
    Handles:
    - Environment-specific settings
    - Secret management
    - Performance optimization
    """
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """
        Generate production configuration
        
        Returns:
            Production configuration dictionary
        """
        return {
            # Database Configuration
            'DATABASE': {
                'url': os.getenv(
                    'PRODUCTION_DATABASE_URL', 
                    'postgresql://coinage:secure_password@db.coinage.com/production'
                ),
                'pool_size': int(os.getenv('DB_POOL_SIZE', 20)),
                'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 10)),
                'pool_timeout': int(os.getenv('DB_POOL_TIMEOUT', 30)),
                'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600))
            },
            
            # Redis Configuration
            'REDIS': {
                'url': os.getenv(
                    'PRODUCTION_REDIS_URL', 
                    'redis://cache.coinage.com:6379/0'
                ),
                'max_connections': int(os.getenv('REDIS_MAX_CONNECTIONS', 100))
            },
            
            # Security Configuration
            'SECURITY': {
                'secret_key': os.getenv(
                    'PRODUCTION_SECRET_KEY', 
                    cls._generate_secret_key()
                ),
                'jwt_expiration': int(os.getenv('JWT_EXPIRATION', 86400)),  # 24 hours
                'password_hash_rounds': int(os.getenv('PASSWORD_HASH_ROUNDS', 12))
            },
            
            # Logging Configuration
            'LOGGING': {
                'level': os.getenv('LOG_LEVEL', 'INFO'),
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'elasticsearch': {
                    'host': os.getenv('ELASTICSEARCH_HOST', 'logs.coinage.com'),
                    'port': int(os.getenv('ELASTICSEARCH_PORT', 9200))
                }
            },
            
            # Performance Configuration
            'PERFORMANCE': {
                'workers': int(os.getenv('GUNICORN_WORKERS', 4)),
                'threads': int(os.getenv('GUNICORN_THREADS', 2)),
                'timeout': int(os.getenv('GUNICORN_TIMEOUT', 120))
            },
            
            # External Services
            'EXTERNAL_SERVICES': {
                'market_data_api': {
                    'url': os.getenv(
                        'MARKET_DATA_API_URL', 
                        'https://api.marketdata.com/v1'
                    ),
                    'api_key': os.getenv('MARKET_DATA_API_KEY')
                },
                'payment_gateway': {
                    'provider': os.getenv('PAYMENT_GATEWAY', 'stripe'),
                    'api_key': os.getenv('PAYMENT_GATEWAY_API_KEY')
                }
            },
            
            # Monitoring Configuration
            'MONITORING': {
                'prometheus': {
                    'host': os.getenv('PROMETHEUS_HOST', 'monitoring.coinage.com'),
                    'port': int(os.getenv('PROMETHEUS_PORT', 9090))
                },
                'jaeger': {
                    'host': os.getenv('JAEGER_HOST', 'tracing.coinage.com'),
                    'port': int(os.getenv('JAEGER_PORT', 6831))
                }
            }
        }
    
    @staticmethod
    def _generate_secret_key() -> str:
        """
        Generate a secure secret key
        
        Returns:
            Cryptographically secure secret key
        """
        import secrets
        return secrets.token_hex(32)
    
    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> bool:
        """
        Validate production configuration
        
        Args:
            config: Configuration dictionary
        
        Returns:
            Configuration validation result
        """
        required_keys = [
            'DATABASE', 
            'REDIS', 
            'SECURITY', 
            'LOGGING', 
            'PERFORMANCE'
        ]
        
        for key in required_keys:
            if key not in config:
                return False
        
        # Additional validation logic
        try:
            # Validate database URL
            assert config['DATABASE']['url'].startswith(('postgresql://', 'mysql://'))
            
            # Validate security settings
            assert len(config['SECURITY']['secret_key']) >= 64
            
            # Validate performance settings
            assert config['PERFORMANCE']['workers'] > 0
            
            return True
        except AssertionError:
            return False

def main():
    """
    Demonstrate production configuration
    """
    config = ProductionConfig.get_config()
    
    # Validate configuration
    is_valid = ProductionConfig.validate_config(config)
    print(f"Configuration Valid: {is_valid}")
    
    # Print sensitive configuration (masked)
    masked_config = {
        k: {
            sk: '***' if 'key' in sk.lower() else sv 
            for sk, sv in v.items()
        } 
        for k, v in config.items()
    }
    
    import json
    print("Production Configuration:")
    print(json.dumps(masked_config, indent=2))

if __name__ == '__main__':
    main()
