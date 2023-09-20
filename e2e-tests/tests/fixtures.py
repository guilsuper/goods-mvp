# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains useful fixtures."""
import os
from typing import Callable

import pytest
import requests
from dotenv import load_dotenv
from selenium import webdriver
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
    """Returns client info and auth tokens."""
    return _client


@pytest.fixture
def sctr_create(client: dict) -> Callable:
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
            headers={"Authorization": f"Bearer {client['tokens']['access']}"}
        ).json()
        return sctr

    return create
