import pytest
from api_tests.clients.api_client import APIClient

client = APIClient()

def test_get_products():
    response = client.get_products()
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_cart_flow():
    user_id = 999
    # Add to cart
    res = client.add_to_cart(user_id, product_id=1, quantity=2)
    assert res.status_code == 200
    assert res.json()["product_id"] == 1
    
    # Get cart
    res = client.get_cart(user_id)
    assert res.status_code == 200
    assert len(res.json()) >= 1

def test_order_flow():
    user_id = 888
    # Ensure cart has items
    client.add_to_cart(user_id, product_id=2, quantity=1)
    
    # Create order
    res = client.create_order(user_id)
    assert res.status_code == 200
    assert res.json()["status"] == "placed"
    assert res.json()["total_amount"] > 0
    
    # Verify cart is empty after order
    cart_res = client.get_cart(user_id)
    assert len(cart_res.json()) == 0
