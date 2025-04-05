import unittest
import json
from app import create_app, db
from app.models import Inventory
from sqlalchemy import text

class InventoryAPITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test environment and create a test client."""
        cls.app = create_app(config_name="testing")
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    def setUp(self):
        """Runs before every test - clears database to ensure a fresh start."""
        with self.app.app_context():
            db.session.rollback()
            db.session.query(Inventory).delete()
            db.session.commit()
    
    def get_auth_token(self):
        """Helper function to retrieve a valid JWT token for authentication."""
        login_response = self.client.post(
            "/login",
            json={"username": "test_user", "password": "test_password"},
        )
        self.assertEqual(login_response.status_code, 200, f"Login failed: {login_response.data}")
        data = login_response.get_json()
        self.assertIsNotNone(data, "Login response JSON is None")
        self.assertIn("token", data, f"Token missing in login response: {data}")
        return data["token"]

    def test_add_product(self):
        """Test adding a product using the API with JWT authentication."""
        token = self.get_auth_token()
        response = self.client.post(
            "/api/products",
            json={
                "item_name": "Test Product",
                "product_code": "123456789",
                "total_stock": 10,
                "unit_price": 19.99,
                "category": "Electronics"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 201, f"Add product failed: {response.data}")
        data = response.get_json()
        self.assertIn("id", data, "Product ID is missing in response")

    def test_search_product(self):
        """Test searching for a product via API."""
        with self.app.app_context():
            db.session.execute(
                text("INSERT INTO inventory (item_name, product_code, total_stock, unit_price, category) "
                     "VALUES ('Test Product', '123456789', 10, 19.99, 'Electronics')")
            )
            db.session.commit()

        response = self.client.get("/api/products?search=Test Product")
        self.assertEqual(response.status_code, 200, f"Search failed: {response.data}")
        data = response.get_json()
        self.assertGreater(len(data), 0, "No products found")

    def test_update_stock(self):
        """Test updating product stock."""
        with self.app.app_context():
            db.session.execute(
                text("INSERT INTO inventory (id, item_name, product_code, total_stock, unit_price, category) "
                     "VALUES (1, 'Test Product', '123456789', 10, 19.99, 'Electronics')")
            )
            db.session.commit()

        token = self.get_auth_token()
        response = self.client.put(
            "/api/products/1",
            json={"total_stock": 15},
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200, f"Stock update failed: {response.data}")
        data = response.get_json()
        self.assertEqual(data["total_stock"], 15, "Stock did not update correctly")

    def tearDown(self):
        """Clean up database sessions after each test."""
        with self.app.app_context():
            db.session.rollback()
            db.session.close()

    @classmethod
    def tearDownClass(cls):
        """Runs after all tests are completed - drops test database."""
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
