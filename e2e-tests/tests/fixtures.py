# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains useful fixtures."""
import json
import os
from time import sleep
from typing import Callable

import pytest
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.utils import init_client
from tests.utils import update_client_info


load_dotenv()


_client = init_client()


@pytest.fixture
def driver():
    """Selenium driver fixture."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    if "SELENIUM_HOST" in os.environ:
        driver = webdriver.Remote(
            command_executor=os.environ["SELENIUM_HOST"],
            options=options,
        )
    else:
        driver = webdriver.Chrome(options=options)

    # default window size is 800x600; set this to 1600x1200
    driver.set_window_size(1600, 1200)

    yield driver
    driver.quit()


@pytest.fixture
def client() -> dict:
    """Returns client info and tokens."""
    # To update the client info after each test
    global _client
    yield _client
    _client = update_client_info(_client)


@pytest.fixture
def signed_in_client(driver: webdriver.Chrome) -> dict:
    """Force sign in the client in the browser and returns its info and tokens."""

    driver.get(os.environ["FRONTEND"] + "/sign-in")
    # e2e tests' data is permanent in a single session
    # This is used to update or create an authorization for a client
    # In case client was authorized
    # If client is signed in, he is not able to visit this link
    if driver.current_url != os.environ["FRONTEND"] + "/sign-in":
        return _client

    # Enter user data
    sign_in_data = {
        "email": _client["email"],
        "password": _client["password"],
    }

    # Enter text to each field
    [
        driver.find_element(By.ID, key).send_keys(sign_in_data[key])
        for key in sign_in_data
    ]

    # Wait until this button is clickable
    sign_in_buttons = driver.find_elements(By.TAG_NAME, "button")
    for element in sign_in_buttons:
        if element.text == "Sign In":
            sign_in_button = element

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(sign_in_button)).click()
    # Wait for an alert
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Successfully logged"
    alert.accept()

    # authTokens is a string that looks like a dict
    # Wait for setting up the localStorage
    for _ in range(5):
        if "authTokens" in driver.execute_script("return window.localStorage;"):
            break
        sleep(1)

    # Update existing tokens, because old tokens aren't valid
    _client["tokens"] = json.loads(
        driver.execute_script("return window.localStorage;")["authTokens"],
    )

    return _client


@pytest.fixture
def origin_report_create_published() -> Callable:
    """Returns a function to configure OriginReport creation using a request to the backend."""
    def create() -> dict:
        """Creates an OriginReport and returns dict with OriginReport info."""
        data = {
            "unique_identifier_type_str": "SKU",
            "unique_identifier": "1aa24a211232aa",
            "short_description": "aaaa",
            "components": [
                {
                    "fraction_cogs": 99,
                    "short_description": "why",
                    "component_type_str": "EXTERNALLY_SOURCED",
                    "external_sku": "aaaaa",
                    "country_of_origin": "US",
                    "company_name": "Mojang",
                },
                {
                    "fraction_cogs": 1,
                    "short_description": "why1",
                    "component_type_str": "MADE_IN_HOUSE",
                    "external_sku": "aaaaa1",
                    "country_of_origin": "CN",  # China
                    "company_name": "Alabama",
                },
            ],
        }
        response = requests.post(
            os.environ["BACKEND"] + "/api/origin_report/create/",
            json=data,
            headers={"Authorization": f"Bearer {_client['tokens']['access']}"},
        )
        response.raise_for_status()
        return response.json()

    return create


@pytest.fixture
def origin_report_create_draft() -> Callable:
    """Returns a function to configure OriginReport draft creation using a
    request to the backend.
    """

    def create() -> dict:
        """Creates an OriginReport draft and returns dict with OriginReport info."""
        data = {
            "unique_identifier_type_str": "SKU",
            "unique_identifier": "123897asdh",
            "short_description": "Iron pan",
            "components": [
                {
                    "fraction_cogs": 80,
                    "short_description": "Iron",
                    "component_type_str": "EXTERNALLY_SOURCED",
                    "external_sku": "aaaaa",
                    "country_of_origin": "US",
                    "company_name": "Mojang",
                },
                {
                    "fraction_cogs": 20,
                    "short_description": "Plastic handle",
                    "component_type_str": "EXTERNALLY_SOURCED",
                    "external_sku": "Polymer",
                    "country_of_origin": "FR",
                    "company_name": "Isort",
                },
            ],
        }
        response = requests.post(
            os.environ["BACKEND"] + "/api/origin_report/create_draft/",
            json=data,
            headers={"Authorization": f"Bearer {_client['tokens']['access']}"},
        )
        response.raise_for_status()
        return response.json()

    return create


@pytest.fixture
def image_path() -> str:
    """Creates temporary image and returns its path"""
    from PIL import Image
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        # Create a simple white image using PIL
        image = Image.new("RGB", (100, 100), "red")

        # Save the image to the temporary file
        image.save(temp_file.name, "PNG")

    return temp_file.name


@pytest.fixture
def company_image(image_path, signed_in_client, driver) -> str:
    """Sets or creates a company image for current client."""
    # Check is company have a logo
    # If not, create it
    if _client["company"]["logo"]:
        return

    edit_url = f"{os.environ['FRONTEND']}/account/company/" \
               f"edit/{signed_in_client['company']['slug']}"

    driver.get(edit_url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "logo")),
    ).send_keys(image_path)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")),
    ).click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Successfully edited"
    alert.accept()

    return image_path
