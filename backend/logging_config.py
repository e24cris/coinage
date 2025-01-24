import logging
import os
import sys
import json
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
import socket

class ContextFilter(logging.Filter):
    """
    Adds contextual information to log records
    """
    def __init__(self):
        super().__init__()
        self.hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = self.hostname
        record.process_id = os.getpid()
        return True

class JsonFormatter(logging.Formatter):
    """
    Custom JSON log formatter for structured logging
    """
    def format(self, record):
        log_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'line': record.lineno,
            'hostname': getattr(record, 'hostname', 'unknown'),
            'process_id': getattr(record, 'process_id', 0)
        }

        # Add exception information if present
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_record)

def setup_logging(log_level=logging.INFO):
    """
    Configure comprehensive logging for the Coinage application
    
    Features:
    - Multiple log handlers
    - Rotating log files
    - JSON structured logging
    - Contextual logging
    """
    # Ensure logs directory exists
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Context filter for additional log information
    context_filter = ContextFilter()

    # JSON Formatter
    json_formatter = JsonFormatter()

    # Console Handler (colored output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.addFilter(context_filter)
    console_handler.setFormatter(json_formatter)

    # Rotating File Handler for all logs
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'coinage_app.log'),
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.addFilter(context_filter)
    file_handler.setFormatter(json_formatter)

    # Time-based Rotating Handler for error logs
    error_handler = TimedRotatingFileHandler(
        os.path.join(logs_dir, 'coinage_errors.log'),
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.addFilter(context_filter)
    error_handler.setFormatter(json_formatter)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=[console_handler, file_handler, error_handler]
    )

    # Create loggers for different components
    loggers = {
        'flask': logging.getLogger('flask'),
        'sqlalchemy': logging.getLogger('sqlalchemy'),
        'app': logging.getLogger('app'),
        'auth': logging.getLogger('auth'),
        'trading': logging.getLogger('trading'),
        'payments': logging.getLogger('payments'),
        'security': logging.getLogger('security')
    }

    # Set log levels
    loggers['flask'].setLevel(logging.WARNING)
    loggers['sqlalchemy'].setLevel(logging.WARNING)
    loggers['app'].setLevel(log_level)
    loggers['auth'].setLevel(log_level)
    loggers['trading'].setLevel(log_level)
    loggers['payments'].setLevel(log_level)
    loggers['security'].setLevel(logging.ERROR)

    return loggers

def get_logger(name):
    """
    Retrieve a logger by name with predefined configuration
    """
    return logging.getLogger(name)

def log_security_event(event_type, details, severity=logging.INFO):
    """
    Log security-related events with enhanced details
    
    Args:
        event_type: Type of security event
        details: Event details dictionary
        severity: Logging severity level
    """
    security_logger = get_logger('security')
    
    event_log = {
        'event_type': event_type,
        'details': details
    }
    
    security_logger.log(severity, json.dumps(event_log))

def main():
    """
    Test logging configuration
    """
    loggers = setup_logging()
    
    # Test different log levels
    loggers['app'].info("Application started")
    loggers['auth'].warning("Login attempt from unknown IP")
    loggers['trading'].error("Trade execution failed")
    
    # Test security event logging
    log_security_event(
        'LOGIN_ATTEMPT', 
        {'username': 'test_user', 'ip_address': '192.168.1.100'}
    )

if __name__ == '__main__':
    main()
