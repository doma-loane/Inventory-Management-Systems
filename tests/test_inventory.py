import pytest

def test_get_inventory(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    assert b"Inventory" in response.data  # Check if "Inventory" is in the response

def test_add_product(client):
    response = client.post('/inventory/add', json={
        "name": "Test Product",
        "category": "Test Category",
        "subcategory": "Test Subcategory",
        "product_code": "TEST123",
        "unit_price": 100.0,
        "total_stock": 50
    })
    assert response.status_code == 201
    assert response.json["message"] == "Product added successfully"

def test_add_product_missing_details(client):
    response = client.post('/inventory/add', json={
        "name": "Incomplete Product"
        # Missing required fields like category, unit_price, and total_stock
    })
    assert response.status_code == 400
    assert response.json["error"] == "Missing product details"

def test_delete_product(client):
    # First, add a product to delete
    add_response = client.post('/inventory/add', json={
        "name": "Product to Delete",
        "category": "Test Category",
        "subcategory": "Test Subcategory",
        "product_code": "DELETE123",
        "unit_price": 50.0,
        "total_stock": 20
    })
    product_id = add_response.json.get("id")

    # Then, delete the product
    delete_response = client.delete(f'/inventory/{product_id}')
    assert delete_response.status_code == 200
    assert delete_response.json["message"] == "Product deleted successfully"

def test_delete_nonexistent_product(client):
    response = client.delete('/inventory/9999')  # Nonexistent product ID
    assert response.status_code == 404
    assert response.json["error"] == "Product not found"

def test_update_stock(client):
    # Add a product first
    add_response = client.post('/inventory/add', json={
        "name": "Product to Update",
        "category": "Test Category",
        "subcategory": "Test Subcategory",
        "product_code": "UPDATE123",
        "unit_price": 50.0,
        "total_stock": 20
    })
    product_id = add_response.json.get("id")

    # Update the stock
    update_response = client.put(f'/inventory/{product_id}/update_stock', json={
        "quantity": 10
    })
    assert update_response.status_code == 200
    assert update_response.json["message"] == "Stock updated successfully"
