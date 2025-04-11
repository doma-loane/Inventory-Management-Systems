import unittest
import pytest

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        from app import create_app
        from app.extensions import db
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        db.init_app(self.app)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Seed the database
            from app.models import User
            from werkzeug.security import generate_password_hash
            user = User(username="testuser", password_hash=generate_password_hash("password"))
            db.session.add(user)
            db.session.commit()

    def login(self):
        return self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'password'
        })

    def test_login_page(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    def tearDown(self):
        from app.extensions import db
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_dashboard_page(self):
        self.login()
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_inventory_page(self):
        self.login()
        response = self.client.get('/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Inventory', response.data)

    def test_add_product_page(self):
        self.login()
        response = self.client.get('/inventory/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add Product', response.data)

    def test_sales_page(self):
        self.login()
        response = self.client.get('/sales')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sales', response.data)

    def test_logout(self):
        self.login()
        response = self.client.get('/api/auth/logout')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged out', response.data)

        # After logout, try accessing dashboard
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertNotIn(b'Dashboard', response.data)
        self.assertTrue(b'Login' in response.data or b'Unauthorized' in response.data)

def test_add_product_page(test_client):
    response = test_client.get("/add_product")  # Ensure the route exists
    assert response.status_code == 200

if __name__ == "__main__":
    unittest.main()
