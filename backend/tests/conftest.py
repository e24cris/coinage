import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.models import Base
from backend.app_integrator import create_app

@pytest.fixture(scope='session')
def app():
    """Create a Flask app for testing"""
    app = create_app('testing')
    return app

@pytest.fixture(scope='session')
def test_database_url():
    """Generate a test database URL"""
    return os.getenv(
        'TEST_DATABASE_URL', 
        'sqlite:///:memory:'
    )

@pytest.fixture(scope='session')
def engine(test_database_url):
    """Create a SQLAlchemy engine for testing"""
    if 'sqlite' in test_database_url:
        # Use in-memory SQLite for testing
        return create_engine(
            test_database_url,
            connect_args={'check_same_thread': False},
            poolclass=StaticPool
        )
    else:
        return create_engine(test_database_url)

@pytest.fixture(scope='session')
def tables(engine):
    """Create tables for testing"""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine, tables):
    """Create a database session for testing"""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

@pytest.fixture
def authenticated_client(client):
    """Create an authenticated test client"""
    # Implement login logic here
    # Example:
    login_data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    response = client.post('/auth/login', json=login_data)
    assert response.status_code == 200
    return client
