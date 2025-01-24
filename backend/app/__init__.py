from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from config.settings import Config
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Create upload directories
    os.makedirs(os.path.join(app.config['BASE_DIR'], 'uploads', 'payment_proofs'), exist_ok=True)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.config['BASE_DIR'], 'uploads')

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    CORS(app)

    # Import and register blueprints
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.trading import trading_bp
    from .routes.payments import payments_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(trading_bp, url_prefix='/trading')
    app.register_blueprint(payments_bp, url_prefix='/payments')

    return app
