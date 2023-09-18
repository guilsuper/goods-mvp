# Copyright 2023 Free World Certified -- all rights reserved.
"""Contains the sign up flow test."""
import os
from typing import Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_flag_displaying(
    driver: webdriver.Chrome,
    sctr_create: Callable,
    company_create: Callable,
    component_create: Callable
):
    """Check for a sign up flow."""
    # SCTR setup, SCTR depends on company and source component
    company = company_create()
    sctr = sctr_create(company["id"])
    component = component_create(sctr["id"])

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
    img_src = "https://cdn.jsdelivr.net/gh/lipis/flag-icons/flags/4x3/" \
              f"{component['country_of_origin'].lower()}.svg"

    flag_img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//img[@src='{img_src}']"))
    )
    assert flag_img
