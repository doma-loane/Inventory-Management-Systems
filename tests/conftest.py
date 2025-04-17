import logging
import pytest
from app import create_app, db
from app.models import Inventory, User
from werkzeug.security import generate_password_hash
from app.config import TestingConfig
from flask import Flask
from dotenv import load_dotenv
from typing import Generator
import os

# Load testing-specific environment variables
load_dotenv(dotenv_path='.env.testing')

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def configure_logging():
    """Configure logging for test runs."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
@pytest.fixture(scope='session')
def app() -> Generator[Flask, None, None]:
    """Creates a Flask app configured for testing."""
    app = create_app('testing')
    with app.app_context():
        yield app  # app context is now usable for any test

@pytest.fixture(scope='session')
def _db(app):
    """Set up and teardown the database (once per session)."""
    db.drop_all()
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

def seed_database():
    """Seed the database with required data for tests."""
    if not Inventory.query.first():
        db.session.add(Inventory(
            item_name="Sample Product",
            category="Sample Category",
            unit_price=10.0,
            total_stock=100,
            product_code="123456789"
        ))
    if not User.query.first():
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("password"),
            role="admin"
        )
        db.session.add(user)
    db.session.commit()

@pytest.fixture(scope='function')
def session(_db):
    """Returns a new session for each test and handles rollback."""
    connection = _db.engine.connect()
    txn = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session
    yield session

    txn.rollback()
    connection.close()
    session.remove()

@pytest.fixture(scope='function')
def client(app):
    """Returns a Flask test client."""
    return app.test_client()

@pytest.fixture(scope='module')
def test_client(app):
    """Provide a test client for the app."""
    with app.test_client() as client:
        yield client

@pytest.fixture
def logged_in_client(test_client):
    """Provide a logged-in client for tests."""
    login_response = test_client.post('/api/auth/login', json={
        'username': 'testuser',  # Match seeded user credentials
        'password': 'password'  # Ensure this matches the test logic
    }, headers={'Content-Type': 'application/json'}, follow_redirects=True)
    assert login_response.status_code == 200, "Login failed"
    return test_client
