import pytest
from app import app  # Replace 'app' with your Flask app module

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_product_endpoint(client):
    response = client.post('/api/inventory/add_product', json={
        'name': 'Test Product',
        'category': 'Test Category',
        'unit_price': 10.99,
        'total_stock': 100
    }, headers={'Content-Type': 'application/json'})
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    assert response.json['message'] == 'Product added'
