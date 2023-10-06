# Copyright 2023 Free World Certified -- all rights reserved.
"""Checks if a user can add the company logo and it will be displayed."""
import os
from typing import Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_company_logo_edit(
    driver: webdriver.Chrome,
    signed_in_client: dict,
    image_path: str,
):
    """Checks if a user can add the company logo and it will be displayed."""
    edit_url = f"{os.environ['FRONTEND']}/account/company/" \
               f"edit/{signed_in_client['company']['slug']}"

    driver.get(edit_url)
    assert driver.current_url == edit_url

    edit_company_logo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "logo")),
    )
    assert edit_company_logo

    edit_company_logo.send_keys(image_path)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")),
    ).click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Successfully edited"
    alert.accept()


def test_company_logo_pages(
    driver: webdriver.Chrome,
    signed_in_client: dict,
    company_image: str,
    origin_report_create_published: Callable,
):
    """Tests if company logo is displayed on info, edit company pages and origin report."""
    # Initialize origin report
    origin_report_id = origin_report_create_published()["id"]

    edit_url = f"{os.environ['FRONTEND']}/account/company/" \
               f"edit/{signed_in_client['company']['slug']}"
    info_url = f"{os.environ['FRONTEND']}/account/company/" \
               f"info/{signed_in_client['company']['slug']}"
    origin_report_url = f"{os.environ['FRONTEND']}/origin_report/{origin_report_id}"

    for url in [edit_url, info_url, origin_report_url]:
        # Check if the company logo is on the company info page
        driver.get(url)
        assert driver.current_url == url

        # The XPATH is designed if the element has multiple classes
        company_logo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//img[contains(concat(' ', normalize-space(@class), ' '), "
                    "' img-thumbnail ')]",
                ),
            ),
        )
        assert company_logo

        # Check if the image is served not by the backend
        for host in [os.environ["BACKEND"], "localhost"]:
            assert host not in company_logo.get_attribute("src")
