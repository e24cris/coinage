import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlAlchemyIntegration

class ProductionMonitor:
    """
    Comprehensive production monitoring system
    
    Features:
    - Error tracking with Sentry
    - Advanced logging
    - Performance monitoring
    - Alert mechanisms
    """

    @staticmethod
    def configure_sentry(app):
        """
        Configure Sentry for error tracking and performance monitoring
        """
        sentry_sdk.init(
            dsn=os.environ.get('SENTRY_DSN', ''),
            integrations=[
                FlaskIntegration(),
                SqlAlchemyIntegration()
            ],
            traces_sample_rate=0.5,  # 50% of transactions
            environment=os.environ.get('FLASK_ENV', 'production'),
            release=os.environ.get('APP_VERSION', 'unknown')
        )

    @staticmethod
    def setup_logging():
        """
        Configure advanced logging for production
        
        Logging Destinations:
        - Console
        - Rotating File Handler
        - Optional: External logging service
        """
        # Configure root logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Rotating File Handler
        file_handler = RotatingFileHandler(
            'coinage_production.log', 
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))

        # Add file handler to root logger
        logging.getLogger().addHandler(file_handler)

    @staticmethod
    def log_critical_event(event_type, details):
        """
        Log critical events with high visibility
        
        Args:
            event_type: Type of critical event
            details: Event details dictionary
        """
        logger = logging.getLogger('CRITICAL_EVENTS')
        logger.critical(f"CRITICAL EVENT: {event_type} - {details}")
        
        # Optional: Send immediate alert via email/SMS
        # Implementation depends on your alerting infrastructure

    @staticmethod
    def performance_tracking(app):
        """
        Add performance tracking middleware
        """
        @app.before_request
        def track_request_performance():
            # Track request start time
            import time
            request_start_time = time.time()
            
            # Store in Flask's g object for end-of-request tracking
            from flask import g
            g.request_start_time = request_start_time

        @app.after_request
        def log_request_performance(response):
            from flask import request, g
            import time
            
            # Calculate request duration
            request_duration = time.time() - g.request_start_time
            
            # Log performance metrics
            logging.getLogger('PERFORMANCE').info(
                f"Path: {request.path}, "
                f"Method: {request.method}, "
                f"Status: {response.status_code}, "
                f"Duration: {request_duration:.4f} seconds"
            )
            
            # Optional: Send to performance monitoring service
            return response

    @staticmethod
    def configure_exception_handlers(app):
        """
        Configure global exception handlers
        """
        @app.errorhandler(Exception)
        def handle_global_exception(e):
            """
            Catch-all exception handler for unhandled exceptions
            """
            logger = logging.getLogger('UNHANDLED_EXCEPTIONS')
            logger.exception(f"Unhandled Exception: {str(e)}")
            
            # Optional: Send immediate alert
            ProductionMonitor.log_critical_event(
                'UNHANDLED_EXCEPTION', 
                {'error': str(e)}
            )
            
            return "An unexpected error occurred", 500

def initialize_production_monitoring(app):
    """
    Initialize all production monitoring features
    """
    ProductionMonitor.configure_sentry(app)
    ProductionMonitor.setup_logging()
    ProductionMonitor.performance_tracking(app)
    ProductionMonitor.configure_exception_handlers(app)

    return app
