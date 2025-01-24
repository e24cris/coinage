from flask import Blueprint, jsonify, render_template

# Create the main blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Main landing page route
    Returns a welcome message or renders the main page
    """
    return jsonify({
        'message': 'Welcome to Coinage Trading Platform',
        'status': 'active'
    }), 200

@main_bp.route('/health')
def health_check():
    """
    Health check endpoint for system status
    """
    return jsonify({
        'status': 'healthy',
        'services': {
            'database': 'connected',
            'authentication': 'enabled'
        }
    }), 200

@main_bp.errorhandler(404)
def not_found_error(error):
    """
    Custom 404 error handler
    """
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource could not be found'
    }), 404

@main_bp.errorhandler(500)
def internal_error(error):
    """
    Custom 500 error handler
    """
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Something went wrong on our end'
    }), 500
