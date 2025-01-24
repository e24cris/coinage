from flask import jsonify, current_app
import traceback
import logging

class ErrorHandler:
    """
    Centralized error handling and logging utility
    
    Features:
    - Standardized error responses
    - Detailed logging
    - Error categorization
    """

    @staticmethod
    def handle_error(error, error_type='GENERIC_ERROR', status_code=500):
        """
        Generate a standardized error response
        
        Args:
            error: Exception or error message
            error_type: Categorized error type
            status_code: HTTP status code
        
        Returns:
            JSON error response
        """
        # Log the full error traceback
        current_app.logger.error(f"Error Type: {error_type}")
        current_app.logger.error(traceback.format_exc())

        # Construct error response
        error_response = {
            'status': 'error',
            'error_code': error_type,
            'message': str(error),
            'details': traceback.format_exc() if current_app.debug else None
        }

        return jsonify(error_response), status_code

    @staticmethod
    def register_error_handlers(app):
        """
        Register global error handlers for the Flask application
        
        Handles:
        - 400 Bad Request
        - 401 Unauthorized
        - 403 Forbidden
        - 404 Not Found
        - 500 Internal Server Error
        """
        @app.errorhandler(400)
        def bad_request(error):
            return ErrorHandler.handle_error(error, 'BAD_REQUEST', 400)

        @app.errorhandler(401)
        def unauthorized(error):
            return ErrorHandler.handle_error(error, 'UNAUTHORIZED', 401)

        @app.errorhandler(403)
        def forbidden(error):
            return ErrorHandler.handle_error(error, 'FORBIDDEN', 403)

        @app.errorhandler(404)
        def not_found(error):
            return ErrorHandler.handle_error(error, 'NOT_FOUND', 404)

        @app.errorhandler(500)
        def internal_server_error(error):
            return ErrorHandler.handle_error(error, 'INTERNAL_SERVER_ERROR', 500)

    @staticmethod
    def log_request(request):
        """
        Log incoming request details for audit and debugging
        
        Args:
            request: Flask request object
        """
        current_app.logger.info(f"Request: {request.method} {request.path}")
        current_app.logger.info(f"Headers: {request.headers}")
        current_app.logger.info(f"Body: {request.get_data(as_text=True)}")

    @staticmethod
    def configure_logging(app):
        """
        Configure application-wide logging
        
        Sets up:
        - Log levels
        - Log format
        - Log destinations
        """
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('coinage_app.log'),
                logging.StreamHandler()
            ]
        )

        # Set Flask app logger
        app.logger.setLevel(logging.INFO)
        
        # Optional: Add custom logging for sensitive operations
        def log_sensitive_action(action, user_id):
            current_app.logger.warning(f"SENSITIVE ACTION: {action} by User {user_id}")

        return log_sensitive_action
