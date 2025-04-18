import unittest
from flask_testing import TestCase
from app import db, create_app  # ✅ Ensure create_app is imported
from app.models import Inventory
import pytest
import logging
from tests.factories import create_inventory_item  # Import the factory function

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class InventoryAPITest(TestCase):
    def create_app(self):
        """Use the app fixture for testing."""
        from app.config import TestingConfig
        return create_app(config_class=TestingConfig)

    def setUp(self):
        """Set up the database before each test."""
        db.create_all()
        # Seed the database
        db.session.add(Inventory(
            item_name="Test Product",  # ✅ Ensure this matches the test case
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

@pytest.mark.usefixtures("client", "db")
def test_add_product(client):
    payload = {
        "item_name": "Test Product",
        "total_stock": 100,
        "unit_price": 10.0,
        "category": "Sample Category",
        "product_code": "123456789"
    }
    response = client.post("/inventory", json=payload)
    assert response.status_code in [200, 201]
    assert b"success" in response.data.lower()

@pytest.mark.usefixtures("client", "db")
def test_sales_dashboard(client):
    create_inventory_item()  # Use the factory to create test data
    response = client.get("/sales/sales")
    assert response.status_code == 200
    assert b"sales" in response.data.lower()

@pytest.mark.parametrize("route,status_code,expected_content", [
    ("/inventory", 200, "Test Product"),
    ("/sales/", 200, "Sales Home"),
    ("/sales/sales", 200, "Sales dashboard")
])
@pytest.mark.usefixtures("client", "db")
def test_routes(client, route, status_code, expected_content):
    if route == "/inventory":
        create_inventory_item(item_name="Test Product")

    response = client.get(route)
    assert response.status_code == status_code
    assert expected_content.lower().encode() in response.data.lower()
