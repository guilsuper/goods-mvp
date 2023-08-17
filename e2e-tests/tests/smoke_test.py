# Copyright 2023 Free World Certified -- all rights reserved.
# Contains smoke test
import os

from selenium import webdriver


def test_smoke(driver: webdriver.Chrome):
    """Checks if frontend home page loads."""
    driver.get(os.environ["FRONTEND"])
    assert "Free World Certified" in driver.title
