import logging
import pytest
from app import create_app, db
from app.models import Inventory, User
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

# Load testing-specific environment variables
load_dotenv(dotenv_path='.env.testing')

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def app():
    """Create a Flask app instance for testing."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use in-memory database for tests
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    with app.app_context():
        db.create_all()  # Ensure tables are created
        seed_database()  # Populate the database with initial data
        yield app
        db.session.remove()
        db.drop_all()  # Clean up after tests

@pytest.fixture(scope="function")
def client(app):
    """Provide a test client for the app."""
    return app.test_client()

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
            password_hash=generate_password_hash("password"),  # Use hashed password
            role="admin"
        )
        db.session.add(user)
    db.session.commit()
