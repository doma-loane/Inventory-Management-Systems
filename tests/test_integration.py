import pytest

@pytest.fixture
def logged_in_client(client):
    # Log in using valid credentials
    login_response = client.post('/login', data={
        'username': 'admin',
        'password': 'adminpass'
    }, follow_redirects=True)
    assert b"Dashboard" in login_response.data or b"Welcome" in login_response.data
    return client

def test_login_page(client):
    # Check that the login page loads
    response = client.get('/login', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

def test_dashboard_page(logged_in_client):
    response = logged_in_client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Dashboard" in response.data

def test_inventory_page(logged_in_client):
    response = logged_in_client.get('/inventory', follow_redirects=True)
    assert response.status_code == 200
    assert b"Inventory" in response.data

def test_add_product_page(logged_in_client):
    response = logged_in_client.get('/add-product', follow_redirects=True)
    assert response.status_code == 200
    assert b"Add New Product" in response.data

def test_sales_page(logged_in_client):
    response = logged_in_client.get('/sales', follow_redirects=True)
    assert response.status_code == 200
    assert b"Process Sale" in response.data

def test_logout(logged_in_client):
    response = logged_in_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    # After logout, user should be on the login page.
    assert b"Login" in response.data

def test_inventory_endpoint(client):
    response = client.get('/api/inventory')
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Ensure the response is a list of inventory items
