# Copyright 2023 Free World Certified -- all rights reserved.
"""Checks if a flag is displayed in the OriginReport page."""
import os
from typing import Callable

from pycountry import countries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_flag_origin_report_info_page(
    driver: webdriver.Chrome,
    origin_report_create_published: Callable,
    client: dict
):
    """Checks if a flag is displayed in the OriginReport info page."""
    origin_report = origin_report_create_published()

    driver.get(os.environ["FRONTEND"] + "/origin_report")

    origin_report_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
                                        f"//a[@href='/origin_report/{origin_report['id']}']"))
    )
    assert origin_report_item

    # After click on a listed OriginReport -- should redirect to OriginReport page
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(origin_report_item)).click()
    assert driver.current_url == os.environ["FRONTEND"] + f"/origin_report/{origin_report['id']}"

    # This url is generated from the coutry code
    # If code isn't in the ISO, there will be no image
    # origin_report has 2 components in components key
    country_code = countries.search_fuzzy(
        origin_report["components"][0]["country_of_origin"])[0].alpha_2

    img_src = "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/" \
              f"{country_code.lower()}.svg"

    flag_img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//img[@src='{img_src}']"))
    )
    assert flag_img


def test_flag_origin_report_create_page(
    driver: webdriver.Chrome,
    signed_in_client: dict
):
    """Checks if a flag is displayed in the OriginReport create page."""

    driver.get(os.environ["FRONTEND"] + "/account/origin_report/create")
    assert driver.current_url == os.environ["FRONTEND"] + "/account/origin_report/create"

    # Find a select element with country code AG and click on it
    # The flag should be displayed after
    country_code = "AG"
    country_option = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             f"//select[@id='country_of_origin']/option[@value='{country_code}']"))
    )
    assert country_option
    country_option.click()

    img_src = "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/" \
              f"{country_code.lower()}.svg"

    flag_img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//img[@src='{img_src}']"))
    )
    assert flag_img


def test_flag_origin_report_edit_page(
    driver: webdriver.Chrome,
    origin_report_create_draft: Callable,
    signed_in_client: dict
):
    """Checks if a flag is displayed in the OriginReport edit page."""
    # Create a draft, so the OriginReport can be edited
    origin_report = origin_report_create_draft()

    # Link to the OriginReport Edit page
    driver.get(os.environ["FRONTEND"] + f"/account/origin_report/edit/{origin_report['id']}")
    assert driver.current_url == os.environ["FRONTEND"] \
        + f"/account/origin_report/edit/{origin_report['id']}"

    # Get existing country code
    country_code = origin_report["components"][0]["country_of_origin"]

    img_src = "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/" \
              f"{country_code.lower()}.svg"

    flag_img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//img[@src='{img_src}']"))
    )
    assert flag_img
