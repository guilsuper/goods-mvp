# Copyright 2023 Free World Certified -- all rights reserved.
"""Checks if a flag is displayed in the SCTR page."""
import os
from typing import Callable

from pycountry import countries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_flag_sctr_info_page(
    driver: webdriver.Chrome,
    sctr_create_published: Callable,
    client: dict
):
    """Checks if a flag is displayed in the SCTR info page."""
    sctr = sctr_create_published()

    driver.get(os.environ["FRONTEND"] + "/sctr")

    sctr_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//a[@href='/sctr/{sctr['id']}']"))
    )
    assert sctr_item

    # After click on a listed SCTR -- should redirect to SCTR page
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(sctr_item)).click()
    assert driver.current_url == os.environ["FRONTEND"] + f"/sctr/{sctr['id']}"

    # This url is generated from the coutry code
    # If code isn't in the ISO, there will be no image
    # sctr has 2 components in components key
    country_code = countries.search_fuzzy(sctr["components"][0]["country_of_origin"])[0].alpha_2

    img_src = "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/" \
              f"{country_code.lower()}.svg"

    flag_img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//img[@src='{img_src}']"))
    )
    assert flag_img


def test_flag_sctr_create_page(
    driver: webdriver.Chrome,
    signed_in_client: dict
):
    """Checks if a flag is displayed in the SCTR create page."""

    driver.get(os.environ["FRONTEND"] + "/account/sctr/create")
    assert driver.current_url == os.environ["FRONTEND"] + "/account/sctr/create"

    # Find a select element with country code AG and click on it
    # The flag should be displayed after
    country_code = "AG"
    driver.find_element(
        By.XPATH, f"//select[@id='country_of_origin']/option[@value='{country_code}']"
    ).click()

    img_src = "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/" \
              f"{country_code.lower()}.svg"

    flag_img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//img[@src='{img_src}']"))
    )
    assert flag_img


def test_flag_sctr_edit_page(
    driver: webdriver.Chrome,
    sctr_create_draft: Callable,
    signed_in_client: dict
):
    """Checks if a flag is displayed in the SCTR edit page."""
    # Create a draft, so the SCTR can be edited
    sctr = sctr_create_draft()

    # Link to the SCTR Edit page
    driver.get(os.environ["FRONTEND"] + f"/account/sctr/edit/{sctr['id']}")
    assert driver.current_url == os.environ["FRONTEND"] + f"/account/sctr/edit/{sctr['id']}"

    # Get existing country code
    country_code = sctr["components"][0]["country_of_origin"]

    img_src = "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/" \
              f"{country_code.lower()}.svg"

    flag_img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//img[@src='{img_src}']"))
    )
    assert flag_img
