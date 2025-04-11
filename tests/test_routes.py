import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models import Inventory

class InventoryAPITest(TestCase):
    def create_app(self):
        """Create the Flask app for testing."""
        return create_app('testing')

    def setUp(self):
        """Set up the database before each test."""
        db.create_all()
        # Seed the database
        db.session.add(Inventory(
            item_name="Sample Product",
            category="Sample Category",
            unit_price=10.0,
            total_stock=100,
            product_code="123456789"
        ))
        db.session.commit()

    def tearDown(self):
        """Clean up the database after each test."""
        db.session.remove()
        db.drop_all()

    def test_add_product(self):
        """Test adding a product using the API."""
        response = self.client.post(
            "/inventory/add",
            json={
                "item_name": "New Product",
                "category": "Electronics",
                "unit_price": 20.0,
                "total_stock": 50
            }
        )
        self.assertEqual(response.status_code, 201)
