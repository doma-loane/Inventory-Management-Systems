import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()  # Ensure the database schema includes the product_code column
    yield app
    with app.app_context():
        db.drop_all()
        db.session.remove()  # Explicitly close the session to resolve warnings

@pytest.fixture
def client(app):
    with app.test_client() as client:
        # Log in the test client
        client.post('/login', data={'username': 'admin', 'password': 'adminpass'})
        yield client
