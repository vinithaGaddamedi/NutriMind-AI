import pytest
from playwright.sync_api import sync_playwright
import os

# Ensure reports directory exists
os.makedirs("reports", exist_ok=True)

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()

    if rep.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_path = f"reports/{item.name}.png"
            page.screenshot(path=screenshot_path)
            print(f"Saved screenshot to {screenshot_path}")
