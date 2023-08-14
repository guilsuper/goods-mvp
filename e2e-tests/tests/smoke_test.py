# Contains smoke test
from selenium import webdriver


def test_smoke(driver: webdriver.Chrome):
    """Checks if frontend home page loads."""
    driver.get("http://frontend:3000/")
    assert "Free World Certified" in driver.title
