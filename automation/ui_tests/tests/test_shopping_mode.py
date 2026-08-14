import pytest

def test_grocery_display(page):
    page.goto("http://localhost:5173/shopping")

    # Clear pantry so we can see all items
    page.fill("input[name='pantry']", "")
    page.click("text=Generate Plan")

    page.wait_for_selector("text=Grains")

    assert page.locator("text=\"Brown Rice\"").is_visible()


def test_pantry_removal(page):
    page.goto("http://localhost:5173/shopping")

    page.fill("input[name='pantry']", "Brown Rice")

    page.click("text=Generate Plan")

    page.wait_for_selector("text=Total: $")
    
    assert not page.locator("text=\"Brown Rice\"").is_visible()


def test_budget_limit(page):
    page.goto("http://localhost:5173/shopping")

    # Set unrealistic budget
    page.fill("input[name='budget']", "10")
    # Clear pantry so we definitely have items to price
    page.fill("input[name='pantry']", "")

    page.click("text=Generate Plan")

    page.wait_for_selector("text=Adjusted")

    assert page.locator("text=Adjusted").is_visible()


def test_checkbox_selection(page):
    page.goto("http://localhost:5173/shopping")
    
    page.fill("input[name='pantry']", "")

    page.click("text=Generate Plan")

    page.wait_for_selector("input[type='checkbox']")

    checkbox = page.locator("input[type='checkbox']").first
    checkbox.check()

    assert checkbox.is_checked()
