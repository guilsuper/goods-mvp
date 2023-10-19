# Copyright 2023 Free World Certified -- all rights reserved.
"""Tests for edit origin report page."""
import os
from typing import Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_edit_page_healthcheck(
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


def test_not_removing_components_after_reload(
    driver: webdriver.Chrome,
    origin_report_create_draft: Callable,
    signed_in_client: dict,
):
    """Go to edit OR page, delete component and reload."""
    origin_report = origin_report_create_draft()

    edit_page_url = os.environ["FRONTEND"] + f"/account/origin_report/edit/{origin_report['id']}"
    driver.get(edit_page_url)
    assert driver.current_url == edit_page_url

    # To wait until all components are loaded; wait for short description
    placeholder = origin_report["components"][0]["short_description"]
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, f"//input[@placeholder='{placeholder}']",
        )),
    )

    # Find 2 buttons that are related to each component
    delete_buttons = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//button[text()='Remove component']")),
    )
    assert len(delete_buttons) == 2
    # Remove first component
    delete_buttons[0].send_keys("\n")

    # Check if component was deleted from the page
    delete_buttons = WebDriverWait(driver, 10).until(
        EC.visibility_of_any_elements_located((By.XPATH, "//button[text()='Remove component']")),
    )
    assert len(delete_buttons) == 1

    # Refresh page and check if 2 component are back
    driver.refresh()
    # To wait until all components are loaded; wait for short description
    placeholder = origin_report["components"][0]["short_description"]
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, f"//input[@placeholder='{placeholder}']",
        )),
    )

    delete_buttons = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//button[text()='Remove component']")),
    )
    assert len(delete_buttons) == 2


def test_single_add_component_button(
    driver: webdriver.Chrome,
    origin_report_create_draft: Callable,
    signed_in_client: dict,
):
    """Go to edit OR page, check is single add component button."""
    origin_report = origin_report_create_draft()

    edit_page_url = os.environ["FRONTEND"] + f"/account/origin_report/edit/{origin_report['id']}"
    driver.get(edit_page_url)
    assert driver.current_url == edit_page_url

    # To wait until all components are loaded; wait for short description
    placeholder = origin_report["components"][0]["short_description"]
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, f"//input[@placeholder='{placeholder}']",
        )),
    )

    add_buttons = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//button[text()='Add component']")),
    )

    assert len(add_buttons) == 1


def test_remove_component_button_if_single_component_only(
    driver: webdriver.Chrome,
    origin_report_create_draft: Callable,
    signed_in_client: dict,
):
    """Go to edit OR page, check if remove button is disabled if 1 component."""
    # Creates draft with 2 components
    origin_report = origin_report_create_draft()

    edit_page_url = os.environ["FRONTEND"] + f"/account/origin_report/edit/{origin_report['id']}"
    driver.get(edit_page_url)
    assert driver.current_url == edit_page_url

    # To wait until all components are loaded; wait for short description
    placeholder = origin_report["components"][0]["short_description"]
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, f"//input[@placeholder='{placeholder}']",
        )),
    )

    # Find 2 buttons that are related to each component
    delete_buttons = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//button[text()='Remove component']")),
    )
    assert len(delete_buttons) == 2
    # Check if first button in the list is not disabled
    # Press it
    assert delete_buttons[0].is_enabled()
    delete_buttons[0].send_keys("\n")

    # Find buttons again and try to press button again
    # Button should be disabled
    delete_buttons = WebDriverWait(driver, 10).until(
        EC.visibility_of_any_elements_located((By.XPATH, "//button[text()='Remove component']")),
    )
    assert len(delete_buttons) == 1

    assert not delete_buttons[0].is_enabled()
