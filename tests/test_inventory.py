from flask_testing import TestCase
from app import create_app, db
from app.models import Inventory

class InventoryTestCase(TestCase):
    def create_app(self):
        """Create the Flask app for testing."""
        return create_app('testing')

    def setUp(self):
        """Set up the database before each test."""
        db.create_all()

    def tearDown(self):
        """Clean up the database after each test."""
        db.session.remove()
        db.drop_all()

    def test_add_product(self):
        """Test adding a product to the inventory."""
        response = self.client.post('/inventory/add', json={
            'item_name': 'Test Product',
            'category': 'Electronics',
            'unit_price': 15.00,
            'total_stock': 5
        })
        self.assertEqual(response.status_code, 201)
        product = Inventory.query.filter_by(item_name='Test Product').first()
        self.assertIsNotNone(product)

    def test_inventory_list(self):
        """Test retrieving the inventory list."""
        product = Inventory(
            item_name='Item X',
            category='Other',
            unit_price=20.0,
            total_stock=10
        )
        db.session.add(product)
        db.session.commit()
        response = self.client.get('/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item X', response.data)
