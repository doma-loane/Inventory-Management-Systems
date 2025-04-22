import unittest
from flask_testing import TestCase
from app import db, create_app  # ✅ Ensure create_app is imported
from app.models import Inventory
import pytest
import logging
from tests.factories import create_inventory_item, create_test_product, create_test_sale  # Import the factory functions

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
def test_add_product(client, db):
    """Test adding a product via the API."""
    # Seed the database if required
    db.session.commit()

    # Make a POST request to add a product
    response = client.post('/api/products', json={
        'name': 'Product A',
        'price': 10.0,
        'stock': 50
    })
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"

@pytest.mark.usefixtures("client", "db")
def test_get_products(client, db):
    """Test retrieving products via the API."""
    # Seed the database with a product
    db.session.add({
        'name': 'Product A',
        'price': 10.0,
        'stock': 50
    })
    db.session.commit()

    # Make a GET request to retrieve products
    response = client.get('/api/products')
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert b'Product A' in response.data

@pytest.mark.usefixtures("client", "app")
def test_add_product(client, app):
    with app.app_context():
        product = create_test_product(app.extensions['sqlalchemy'].db)
        assert product.name == "Test Product"

@pytest.mark.usefixtures("client", "app")
def test_sales_dashboard(client, app):
    with app.app_context():
        db = app.extensions['sqlalchemy'].db
        product = create_test_product(db)
        sale = create_test_sale(db, product.id)

    response = client.get('/sales/sales')
    assert response.status_code == 200
    assert b"Sales dashboard" in response.data

@pytest.mark.parametrize("route,status_code,expected_content", [
    ("/inventory", 200, b"Test Product"),
    ("/sales/", 200, b"Sales Home"),
    ("/sales/sales", 200, b"Sales dashboard")
])
@pytest.mark.usefixtures("client", "app")
def test_routes(client, app, route, status_code, expected_content):
    with app.app_context():
        db = app.extensions['sqlalchemy'].db
        product = create_test_product(db)
        sale = create_test_sale(db, product.id)

    response = client.get(route)
    assert response.status_code == status_code
    assert expected_content in response.data
