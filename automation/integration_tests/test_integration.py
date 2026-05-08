import pytest
from api_tests.clients.api_client import APIClient
from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.product_page import ProductPage

# Scenario 1: Create order via API, validate in UI (Mocked as UI verification logic)
# Scenario 2: Add item via UI, validate cart via API

client = APIClient()

def test_add_via_ui_validate_via_api(page):
    user_id = 1 # Setup in login component statically for MVP
    
    # Ensure cart is clean (simulated)
    # In real app we would clear cart via DB or API
    
    # UI actions
    login_page = LoginPage(page)
    login_page.login("testuser")
    
    product_page = ProductPage(page)
    product_page.add_first_product_to_cart()
    
    # API validation
    res = client.get_cart(user_id)
    assert res.status_code == 200
    # The cart should have at least the item we just added
    assert len(res.json()) > 0
