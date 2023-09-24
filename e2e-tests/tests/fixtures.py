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


load_dotenv()


_client = init_client()


@pytest.fixture
def driver():
    """Selenium driver fixture."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def client() -> dict:
    """Returns client info and tokens."""
    return _client


@pytest.fixture
def signed_in_client(driver: webdriver.Chrome) -> dict:
    """Force sign in the client in the browser and returns its info and tokens."""

    driver.get(os.environ["FRONTEND"] + "/sign-in")

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
        driver.execute_script("return window.localStorage;")["authTokens"]
    )

    return _client


@pytest.fixture
def sctr_create_published() -> Callable:
    """Returns a function to configure SCTR creation using a request to the backend."""
    def create() -> dict:
        """Creates an SCTR and returns dict with SCTR info."""
        data = {
            "unique_identifier_type_str": "SKU",
            "unique_identifier": "1aa24a211232aa",
            "marketing_name": "aaaa",
            "components": [
                {
                    "fraction_cogs": 99,
                    "marketing_name": "why",
                    "component_type_str": "EXTERNALLY_SOURCED",
                    "external_sku": "aaaaa",
                    "country_of_origin": "USA",
                    "company_name": "Mojang"
                },
                {
                    "fraction_cogs": 1,
                    "marketing_name": "why1",
                    "component_type_str": "MADE_IN_HOUSE",
                    "external_sku": "aaaaa1",
                    "country_of_origin": "China",
                    "company_name": "Alabama"
                }
            ]
        }
        sctr = requests.post(
            os.environ["BACKEND"] + "/api/sctr/create/",
            json=data,
            headers={"Authorization": f"Bearer {_client['tokens']['access']}"}
        ).json()
        return sctr

    return create


@pytest.fixture
def sctr_create_draft() -> Callable:
    """Returns a function to configure SCTR draft creation using a request to the backend."""
    def create() -> dict:
        """Creates an SCTR draft and returns dict with SCTR info."""
        data = {
            "unique_identifier_type_str": "SKU",
            "unique_identifier": "1aa24a211232aa",
            "marketing_name": "aaaa",
            "components": [
                {
                    "fraction_cogs": 99,
                    "marketing_name": "why",
                    "component_type_str": "EXTERNALLY_SOURCED",
                    "external_sku": "aaaaa",
                    "country_of_origin": "USA",
                    "company_name": "Mojang"
                }
            ]
        }
        sctr = requests.post(
            os.environ["BACKEND"] + "/api/sctr/create_draft/",
            json=data,
            headers={"Authorization": f"Bearer {_client['tokens']['access']}"}
        ).json()
        return sctr

    return create
