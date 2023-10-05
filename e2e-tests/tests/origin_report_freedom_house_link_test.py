# Copyright 2023 Free World Certified -- all rights reserved.
"""Checks if freedomhouse link is displayed in the OriginReport page."""
import os
from typing import Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.utils import get_country_data


def test_freedom_house_links_origin_report_info_page(
    driver: webdriver.Chrome,
    origin_report_create_published: Callable,
    client: dict,
):
    """Checks if a freedom house links are displayed in the OriginReport info page."""

    # fetch the country data from the backend
    country_data = get_country_data()

    origin_report = origin_report_create_published()

    driver.get(os.environ["FRONTEND"] + "/origin_report")

    origin_report_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH,
            f"//a[@href='/origin_report/{origin_report['id']}']",
        )),
    )
    assert origin_report_item

    # After click on a listed OriginReport -- should redirect to OriginReport page
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(origin_report_item)).click()
    assert driver.current_url == os.environ["FRONTEND"] + f"/origin_report/{origin_report['id']}"

    # Verify the freedom house url is valid for each component
    for component in origin_report["components"]:
        assert component["country_of_origin"] in country_data
        country = country_data[component["country_of_origin"]]
        fh_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//a[@href='https://freedomhouse.org/country/{country['freedom_house_url_name']}"
                f"/freedom-world/2023']",
            )),
        )
        assert fh_link
