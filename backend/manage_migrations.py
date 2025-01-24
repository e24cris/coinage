from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app, db

# Create the Flask application
app = create_app()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Flask-Script Manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # Import models to ensure they are recognized by SQLAlchemy
    from app.models.user import User, TradingAccount, TradingPosition, Transaction, ManualPaymentRequest
    
    manager.run()
