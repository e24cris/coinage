import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///coinage.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define initial database models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Investment(Base):
    __tablename__ = "investments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    asset_type = Column(String)
    amount = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_tables():
    """
    Create all database tables
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        return False

def seed_initial_data():
    """
    Seed initial database data
    """
    db = SessionLocal()
    try:
        # Create initial admin user if not exists
        admin_user = User(
            username='coinage_admin',
            email='admin@coinage.com',
            hashed_password='secure_initial_password_hash'
        )
        db.add(admin_user)
        db.commit()
        logger.info("Initial admin user created")
        return True
    except Exception as e:
        logger.error(f"Error seeding initial data: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    """
    Main database migration script
    """
    logger.info("Starting Coinage Database Migration")
    
    # Create tables
    if not create_tables():
        logger.critical("Database table creation failed")
        return False
    
    # Seed initial data
    if not seed_initial_data():
        logger.critical("Initial data seeding failed")
        return False
    
    logger.info("Database migration completed successfully")
    return True

if __name__ == '__main__':
    main()
