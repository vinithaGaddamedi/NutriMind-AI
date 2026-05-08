import pytest

def test_store_route_and_price_comparison(page):
    # Navigate to shopping mode
    page.goto("http://localhost:5173/shopping")
    
    # Wait for page to load
    page.wait_for_selector("text=Smart Shopping Mode")
    
    # Generate plan
    page.click("data-testid=generate-plan")
    
    # Wait for route optimization headers (e.g., Aisle-by-Aisle Route)
    page.wait_for_selector("text=Aisle-by-Aisle Route")
    
    # Validate a specific aisle is visible (e.g., Produce or Dairy)
    assert page.locator("text=Produce").is_visible() or page.locator("text=Dairy").is_visible()
    
    # Validate Price Comparison block is present
    assert page.locator("text=Price Comparison").is_visible()
    
    # Validate the 'Best Store' tag is visible
    assert page.locator("text=Best Store").is_visible()
