import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()
        db.session.remove()

@pytest.fixture
def client(app):
    with app.test_client() as client:      
        yield client
