from flask import Flask
from app import create_app, db

def create_test_app():
    """Create and configure a test instance of the Flask application."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use in-memory SQLite for testing
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all()  # Create tables
    return app

def teardown_test_app(app):
    """Tear down the test application."""
    with app.app_context():
        db.session.remove()
        db.drop_all()
