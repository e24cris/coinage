import os
import logging
import json
import socket
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import requests
from elasticsearch import Elasticsearch
from pythonjsonlogger import jsonlogger

class LogManager:
    """
    Comprehensive Log Management System
    
    Features:
    - Multi-destination logging
    - Structured JSON logging
    - Remote log shipping
    - Log rotation
    - Centralized configuration
    """
    
    def __init__(self, app_name='coinage', log_dir=None):
        """
        Initialize log management system
        
        Args:
            app_name: Name of the application
            log_dir: Directory for log storage
        """
        self.app_name = app_name
        self.hostname = socket.gethostname()
        
        # Default log directory
        if log_dir is None:
            log_dir = os.path.join(
                os.path.dirname(__file__), 
                'logs', 
                self.app_name
            )
        
        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)
        self.log_dir = log_dir
        
        # Elasticsearch configuration
        self.es_client = self._setup_elasticsearch()
        
        # Logging configuration
        self.logger = self._configure_logging()
    
    def _setup_elasticsearch(self):
        """
        Setup Elasticsearch client for log shipping
        
        Returns:
            Elasticsearch client or None
        """
        try:
            es_host = os.getenv('ELASTICSEARCH_HOST', 'localhost')
            es_port = int(os.getenv('ELASTICSEARCH_PORT', 9200))
            
            return Elasticsearch([{
                'host': es_host,
                'port': es_port
            }])
        except Exception as e:
            logging.error(f"Elasticsearch connection failed: {e}")
            return None
    
    def _configure_logging(self):
        """
        Configure comprehensive logging system
        
        Returns:
            Configured logger
        """
        # JSON Formatter
        json_formatter = jsonlogger.JsonFormatter(
            fmt='%(asctime)s %(levelname)s %(name)s %(message)s',
            json_ensure_ascii=False
        )
        
        # Root Logger
        logger = logging.getLogger(self.app_name)
        logger.setLevel(logging.INFO)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(json_formatter)
        logger.addHandler(console_handler)
        
        # Rotating File Handler
        file_handler = RotatingFileHandler(
            os.path.join(self.log_dir, f'{self.app_name}.log'),
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)
        
        # Error Log Handler
        error_handler = TimedRotatingFileHandler(
            os.path.join(self.log_dir, f'{self.app_name}_errors.log'),
            when='midnight',
            interval=1,
            backupCount=30
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(json_formatter)
        logger.addHandler(error_handler)
        
        return logger
    
    def log(self, level, message, extra=None):
        """
        Log message with optional extra context
        
        Args:
            level: Logging level
            message: Log message
            extra: Additional context dictionary
        """
        log_data = {
            'app_name': self.app_name,
            'hostname': self.hostname,
            'message': message
        }
        
        if extra:
            log_data.update(extra)
        
        # Log to configured handlers
        if level == logging.INFO:
            self.logger.info(json.dumps(log_data))
        elif level == logging.WARNING:
            self.logger.warning(json.dumps(log_data))
        elif level == logging.ERROR:
            self.logger.error(json.dumps(log_data))
        
        # Ship logs to Elasticsearch
        self._ship_log_to_elasticsearch(level, log_data)
    
    def _ship_log_to_elasticsearch(self, level, log_data):
        """
        Ship logs to Elasticsearch
        
        Args:
            level: Log level
            log_data: Log data dictionary
        """
        if self.es_client:
            try:
                self.es_client.index(
                    index=f'{self.app_name}-logs-{datetime.now().strftime("%Y.%m.%d")}',
                    body=log_data
                )
            except Exception as e:
                logging.error(f"Log shipping to Elasticsearch failed: {e}")
    
    def log_security_event(self, event_type, details):
        """
        Log security-related events
        
        Args:
            event_type: Type of security event
            details: Event details dictionary
        """
        security_log = {
            'event_type': event_type,
            'details': details
        }
        
        self.log(logging.ERROR, "SECURITY_EVENT", security_log)
    
    def send_alert(self, message, severity='info'):
        """
        Send alerts via multiple channels
        
        Args:
            message: Alert message
            severity: Alert severity
        """
        # Slack notification
        slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
        if slack_webhook:
            try:
                requests.post(slack_webhook, json={
                    'text': f"*{severity.upper()} Alert*: {message}"
                })
            except Exception as e:
                self.log(logging.ERROR, f"Slack alert failed: {e}")
        
        # Email notification can be added similarly
    
    @classmethod
    def get_instance(cls, app_name='coinage'):
        """
        Singleton pattern for log manager
        
        Args:
            app_name: Name of the application
        
        Returns:
            LogManager instance
        """
        if not hasattr(cls, '_instance'):
            cls._instance = cls(app_name)
        return cls._instance

def main():
    """
    Demonstrate log management capabilities
    """
    log_manager = LogManager.get_instance()
    
    # Log different levels
    log_manager.log(logging.INFO, "Application started")
    log_manager.log(logging.WARNING, "High CPU usage detected")
    log_manager.log(logging.ERROR, "Database connection failed")
    
    # Log security event
    log_manager.log_security_event(
        'LOGIN_ATTEMPT', 
        {'username': 'test_user', 'status': 'failed'}
    )
    
    # Send alert
    log_manager.send_alert("System performance degraded", "warning")

if __name__ == '__main__':
    main()
