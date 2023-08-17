# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains useful fixtures."""
import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    """Selenium driver fixture."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
