import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:5173"

def test_full_e2e_shopping_flow(page: Page):
    """
    Test the entire end-to-end user journey:
    Dashboard -> Meal Planner -> Pantry Check -> Shopping Mode -> Cart -> Order -> Tracking
    """
    # 1. Login (Assuming mock login uses 'demo' user)
    page.goto(f"{BASE_URL}/login")
    
    # Wait for login button
    login_button = page.locator("button", has_text="Login")
    expect(login_button).to_be_visible(timeout=10000)
    
    # Fill username
    page.fill("input[id='username']", "e2e_user")
    login_button.click()
        
    # Wait for Dashboard to load
    expect(page).to_have_url(f"{BASE_URL}/dashboard")
    expect(page.locator("h1").first).to_contain_text("Welcome to your Dashboard", timeout=10000)
    
    # 2. Go to Meal Planner
    page.click("h3:has-text('AI Meal Planner')")
    expect(page).to_have_url(f"{BASE_URL}/meal-planner")
    expect(page.locator("h2").first).to_contain_text("Nutrition Meal Planner", timeout=10000)
    
    # Fill in profile details (if not pre-filled)
    page.fill("input[name='name']", "Test User")
    page.fill("input[name='age']", "30")
    page.fill("input[name='weight']", "75")
    page.fill("input[name='height']", "175")
    
    # Generate Plan
    page.click("button:has-text('Generate Weekly Plan')")
    
    # Wait for the plan to load (checking for 'Monday')
    expect(page.locator("h4:has-text('Monday')").first).to_be_visible(timeout=10000)
    
    # 3. Proceed to Pantry
    page.click("button:has-text('Proceed to Pantry')")
    expect(page).to_have_url(f"{BASE_URL}/pantry")
    expect(page.locator("h1")).to_contain_text("Smart Pantry Check")
    
    # Mark the first item as 'In Stock'
    in_stock_button = page.locator("button:has-text('In Stock ✓')").first
    expect(in_stock_button).to_be_visible(timeout=10000)
    in_stock_button.click()
    
    # 4. Save and Proceed to Shopping
    page.click("button:has-text('Save & Proceed to Shopping')")
    expect(page).to_have_url(f"{BASE_URL}/shopping")
    expect(page.locator("h2").first).to_contain_text("Smart Shopping Mode", timeout=10000)
    
    # Wait for shopping plan to generate and display categories
    expect(page.locator("button:has-text('Add All Checked & Checkout')")).to_be_visible(timeout=10000)
    
    # 5. Add to Cart and Checkout
    page.click("button:has-text('Add All Checked & Checkout')")
    
    # Wait for Cart page
    expect(page).to_have_url(f"{BASE_URL}/cart")
    expect(page.locator("h2").first).to_contain_text("Your Smart Cart", timeout=10000)
    
    # 6. Final Checkout
    page.click("button:has-text('Checkout')")
    
    # Wait for Order Success
    expect(page).to_have_url(f"{BASE_URL}/order-success")
    expect(page.locator("h1").first).to_contain_text("Order Placed Successfully!", timeout=10000)
    
    # 7. Track Orders
    page.click("button:has-text('Track Order')")
    expect(page.locator("h1").first).to_contain_text("Your Orders")
    
    # Verify the order exists in the list
    expect(page.locator("div.glass-panel").first).to_be_visible()
