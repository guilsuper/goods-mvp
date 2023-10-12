# Copyright 2023 Free World Certified -- all rights reserved.
"""Tests for edit origin report page."""
import os
from typing import Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_edit_page(
    driver: webdriver.Chrome,
    origin_report_create_draft: Callable,
    signed_in_client: dict,
):
    """Go to edit OR page, edit field."""
    origin_report = origin_report_create_draft()
    new_fraction_cogs = 110

    edit_page_url = os.environ["FRONTEND"] + f"/account/origin_report/edit/{origin_report['id']}"
    driver.get(edit_page_url)
    assert driver.current_url == edit_page_url

    # Find a component field
    fraction_cogs = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.ID,
            "fraction_cogs",
        )),
    )
    # Delete old values
    fraction_cogs.send_keys(Keys.CONTROL + "a")
    fraction_cogs.send_keys(Keys.DELETE)
    # Set new value
    fraction_cogs.send_keys(new_fraction_cogs)

    assert fraction_cogs.get_attribute("value") == str(new_fraction_cogs)
