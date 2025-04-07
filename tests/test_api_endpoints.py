import pytest
from app import app  # Replace 'app' with your Flask app module

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_product_endpoint(client):
    response = client.post('/add_product', data={
        'name': 'Test Product',
        'category': 'Test Category',
        'unit_price': 10.99,
        'total_stock': 100
    })
    assert response.status_code == 200
    assert response.json['success'] is True
    assert 'Product added successfully' in response.json['message']
