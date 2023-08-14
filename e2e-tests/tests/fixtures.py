"""Module contains useful fixtures."""
import pytest
from dotenv import find_dotenv
from dotenv import load_dotenv
from selenium import webdriver


# Parse a .env file,
# then load all the variables found as environment variables.
# Search in increasingly higher folders for the given file (.env by default)
load_dotenv(find_dotenv())


@pytest.fixture
def driver():
    """Selenium driver fixture."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
