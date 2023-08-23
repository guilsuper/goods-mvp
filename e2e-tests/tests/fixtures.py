# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains useful fixtures."""
import os

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


@pytest.fixture
def temp_email():
    """Setup for temporary email."""
    # Returns email address to use for accessing the mail inbox

    return os.environ["EMAIL_RECEIVER"]
