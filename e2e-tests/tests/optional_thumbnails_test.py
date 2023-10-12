# Copyright 2023 Free World Certified -- all rights reserved.
"""Check if thumbnails are optional for creating a draft OR."""
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_optional_thumbnails(
    driver: webdriver.Chrome,
    signed_in_client: dict,
):
    """Test if thumbnails are optional for creating a draft."""
    create_url = f"{os.environ['FRONTEND']}/account/origin_report/create"
    driver.get(create_url)

    assert driver.current_url == create_url

    # Set basic information
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "unique_identifier")),
    ).send_keys("asdaskdasdj")

    # Create a draft
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Create Draft']")),
    ).send_keys("\n")

    # Check if draft was created
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Successfully created"
    alert.accept()
