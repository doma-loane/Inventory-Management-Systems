def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Dashboard" in response.data  # Check if "Dashboard" is in the response
