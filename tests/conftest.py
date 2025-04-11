import logging
import pytest
from app import create_app, db
from app.models import Inventory, User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='session')
def configure_logging():
    """Configure logging for test runs."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)

@pytest.fixture(scope='session')
def app():
    """Create a Flask app instance for testing."""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        yield app

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
def session(app):
    """Provide a database session for each test."""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Provide a test client for each test."""
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

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
