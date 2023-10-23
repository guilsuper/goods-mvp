# Copyright 2023 Free World Certified -- all rights reserved.
"""Check for OR thumbnails."""
import os
from io import BytesIO

import numpy
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from tests.utils import compare_images


def test_origin_report_thumbnails(
    driver: webdriver.Chrome,
    signed_in_client: dict,
    image_path: str,
):
    """Checks OR thumbnails."""
    create_url = f"{os.environ['FRONTEND']}/account/origin_report/create"
    identifier = "aaaaaa"

    driver.get(create_url)
    assert driver.current_url == create_url

    # Set required information
    identifier_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "unique_identifier")),
    )
    assert identifier_field
    identifier_field.send_keys(identifier)

    country_of_origin = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "country_of_origin")),
    )
    assert country_of_origin
    Select(country_of_origin).select_by_visible_text("Albania")

    thumbnail = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "thumbnail")),
    )
    assert thumbnail
    thumbnail.send_keys(image_path)

    create_draft_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Create Draft']")),
    )
    assert create_draft_button
    create_draft_button.click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Successfully created"
    alert.accept()

    assert driver.current_url == f"{os.environ['FRONTEND']}/account/origin_report"

    origin_report = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, f"//a[div[text() = 'Identifier: {identifier}']]",
        )),
    )
    assert origin_report

    thumbnail = origin_report.find_element(By.TAG_NAME, "img")
    assert thumbnail

    img_reference = Image.open(image_path)

    # Get logo directly by media url in the company info page
    src = thumbnail.get_attribute("src")
    response = requests.get(src)
    image_data = response.content
    img_test = Image.open(BytesIO(image_data))

    # numpy.isclose is used to set the error
    # that is close to 0
    assert numpy.isclose(compare_images(img_reference, img_test), 0)

    # Move to OR info page
    origin_report.send_keys("\n")

    assert "/origin_report/" in driver.current_url

    src = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, "//img[@alt='Thumbnail']",
        )),
    ).get_attribute("src")

    response = requests.get(src)
    image_data = response.content
    img_test = Image.open(BytesIO(image_data))
    assert numpy.isclose(compare_images(img_reference, img_test), 0)

    edit_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Edit']")),
    )
    assert edit_link
    edit_link.send_keys("\n")

    assert "/account/origin_report/edit/" in driver.current_url

    src = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, "//img[@alt='Thumbnail']",
        )),
    ).get_attribute("src")

    response = requests.get(src)
    image_data = response.content
    img_test = Image.open(BytesIO(image_data))
    assert numpy.isclose(compare_images(img_reference, img_test), 0)
