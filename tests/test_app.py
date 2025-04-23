import unittest
from flask_testing import TestCase
from app import create_app, db

class AppTest(TestCase):
    def create_app(self):
        """Create the Flask app for testing."""
        return create_app(config_name="testing")

    def setUp(self):
        """Set up the database before each test."""
        db.create_all()

    def tearDown(self):
        """Clean up the database after each test."""
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        """Test the home page route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)
