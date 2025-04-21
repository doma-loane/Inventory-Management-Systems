import logging
import pytest
from app import create_app, db as _db
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

@pytest.fixture(scope="session")
def app() -> Generator[Flask, None, None]:
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.getenv("TEST_DATABASE_URI", "sqlite:///test.db"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    # ✅ Push context for database setup
    with app.app_context():
        yield app

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

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
def session(db):
    """Returns a new session for each test and handles rollback."""
    connection = db.engine.connect()
    txn = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session
    yield session

    txn.rollback()
    connection.close()
    session.remove()

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
