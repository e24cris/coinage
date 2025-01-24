import os
import sys
import threading
from flask import Flask, request, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import our custom modules
from environment_config import EnvironmentConfig
from log_management import LogManager
from monitoring_dashboard import MonitoringDashboard
from security_audit import SecurityAudit
from comprehensive_testing import ComprehensiveTestSuite
from logging_config import setup_logging

class CoinageApplicationIntegrator:
    """
    Centralized Application Integration Framework
    
    Responsible for:
    - Configuration Management
    - Logging
    - Monitoring
    - Security
    - Testing
    """
    
    def __init__(self, env='development'):
        """
        Initialize Coinage Application
        
        Args:
            env: Environment type (development, staging, production)
        """
        # Load environment configuration
        self.config = EnvironmentConfig.load_environment(env)
        
        # Initialize logging
        self.log_manager = LogManager.get_instance()
        
        # Initialize Flask application
        self.app = self._create_flask_app()
        
        # Initialize database
        self.db = self._setup_database()
        
        # Initialize monitoring
        self.monitoring_dashboard = self._setup_monitoring()
        
        # Security audit
        self.security_audit = self._run_security_audit()
    
    def _create_flask_app(self):
        """
        Create and configure Flask application
        
        Returns:
            Configured Flask application
        """
        app = Flask(__name__)
        
        # Apply configuration
        app.config.update(self.config)
        
        # Enable CORS
        CORS(app, resources={
            r"/*": {
                "origins": self.config.get('CORS_ORIGINS', '*'),
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"]
            }
        })
        
        # Request logging middleware
        @app.before_request
        def log_request_info():
            """Log each request"""
            request_info = {
                'method': request.method,
                'path': request.path,
                'remote_addr': request.remote_addr
            }
            self.log_manager.log(
                logging.INFO, 
                "Incoming Request", 
                request_info
            )
        
        # Error handling
        @app.errorhandler(Exception)
        def handle_exception(e):
            """Global error handler"""
            error_info = {
                'error_type': type(e).__name__,
                'error_message': str(e)
            }
            self.log_manager.log(
                logging.ERROR, 
                "Unhandled Exception", 
                error_info
            )
            return "An unexpected error occurred", 500
        
        return app
    
    def _setup_database(self):
        """
        Setup SQLAlchemy database connection
        
        Returns:
            Configured SQLAlchemy database instance
        """
        db = SQLAlchemy(self.app)
        Migrate(self.app, db)
        
        # Log database connection
        try:
            db.engine.connect()
            self.log_manager.log(
                logging.INFO, 
                "Database Connection Established"
            )
        except Exception as e:
            self.log_manager.log(
                logging.ERROR, 
                f"Database Connection Failed: {e}"
            )
        
        return db
    
    def _setup_monitoring(self):
        """
        Setup application monitoring
        
        Returns:
            Monitoring dashboard instance
        """
        external_services = [
            'https://api.coinage.com/health',
            'https://database.coinage.com/status',
            'https://auth.coinage.com/ping'
        ]
        
        dashboard = MonitoringDashboard()
        
        # Start monitoring in a separate thread
        monitoring_thread = threading.Thread(
            target=dashboard.start_monitoring, 
            args=(external_services,),
            daemon=True
        )
        monitoring_thread.start()
        
        return dashboard
    
    def _run_security_audit(self):
        """
        Run comprehensive security audit
        
        Returns:
            Security audit instance
        """
        audit = SecurityAudit(os.path.dirname(__file__))
        
        # Run audit in a separate thread to avoid blocking
        audit_thread = threading.Thread(
            target=audit.run_full_audit,
            daemon=True
        )
        audit_thread.start()
        
        return audit
    
    def register_blueprints(self, blueprints):
        """
        Register Flask blueprints
        
        Args:
            blueprints: List of Flask blueprints
        """
        for blueprint in blueprints:
            self.app.register_blueprint(blueprint)
    
    def run_tests(self):
        """
        Run comprehensive test suite
        """
        test_suite = ComprehensiveTestSuite(
            base_url=f"http://localhost:{self.config.get('PORT', 5000)}"
        )
        
        try:
            test_suite.run_comprehensive_test()
            self.log_manager.log(
                logging.INFO, 
                "Comprehensive Test Suite Passed"
            )
        except Exception as e:
            self.log_manager.log(
                logging.ERROR, 
                f"Test Suite Failed: {e}"
            )
    
    def start(self, port=None):
        """
        Start the Flask application
        
        Args:
            port: Port to run the application (optional)
        """
        # Use port from config or default
        run_port = port or self.config.get('PORT', 5000)
        
        # Log application start
        self.log_manager.log(
            logging.INFO, 
            f"Starting Coinage Application on port {run_port}"
        )
        
        # Run tests before starting (optional)
        if self.config.get('RUN_TESTS_ON_START', False):
            self.run_tests()
        
        # Start Flask application
        self.app.run(
            host='0.0.0.0', 
            port=run_port, 
            debug=self.config.get('DEBUG', False)
        )

def main():
    """
    Main application entry point
    """
    # Detect environment from environment variable
    env = os.getenv('FLASK_ENV', 'development')
    
    # Initialize and start application
    app_integrator = CoinageApplicationIntegrator(env)
    
    # Optional: Add blueprints here
    # app_integrator.register_blueprints([auth_blueprint, trading_blueprint])
    
    # Start the application
    app_integrator.start()

if __name__ == '__main__':
    main()
