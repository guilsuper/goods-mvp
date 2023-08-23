# Copyright 2023 Free World Certified -- all rights reserved.
"""Contains the sign up flow test."""
import os
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.utils import get_emails
from tests.utils import read_email


def test_sign_up_correct(driver: webdriver.Chrome, temp_email):
    """Check for a sign up flow."""
    driver.get(os.environ["FRONTEND"])

    # Healthcheck
    assert "Free World Certified" in driver.title

    # Check if sign-up button exists
    # It shoul lead to /sign-up url
    button = driver.find_element(By.XPATH, "//a[@href='/sign-up']")
    assert button

    # After click -- should redirect to sign-up page
    driver.execute_script("arguments[0].click();", button)
    assert driver.current_url == os.environ["FRONTEND"] + "/sign-up"

    # Check if all 5 fields exist
    sign_up_fields_ids = [
        "email",
        "password",
        "website",
        "company_name",
        "jurisdiction"
    ]
    field_elements = [driver.find_element(By.ID, id_) for id_ in sign_up_fields_ids]
    assert all(field_elements)

    # Check if sign-up button exists
    sign_up_buttons = driver.find_elements(By.TAG_NAME, "button")
    for element in sign_up_buttons:
        if element.text == "Sign Up":
            sign_up_button = element

    assert sign_up_button

    # Enter user data
    sign_up_data = {
        "email": temp_email,
        "password": "1234",
        "website": "website.com",
        "company_name": "company name inc",
        "jurisdiction": "Georgia, USA"
    }

    # Enter text to each field
    [
        el.send_keys(sign_up_data[key])
        for el, key in zip(field_elements, sign_up_data)
    ]

    # Wait until this button is clickable
    driver.execute_script("arguments[0].click();", sign_up_button)

    # Wait for an alert
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    # Wait for email to get
    for _ in range(10):
        time.sleep(1)
        messages = get_emails()

        # If there is unread message from the website email
        if messages:
            break

    # If no unread messages from the website email
    assert messages

    text = read_email(messages[0])
    assert text

    regex = re.compile("(/activated/[a-zA-Z]{0,4}/[0-9a-zA-Z_-]+$)")
    link = os.environ["FRONTEND"] + regex.search(text).group(1)
    driver.get(link)

    # Check if sign-in button exists
    # It shoul lead to /sign-in url
    button = driver.find_element(By.XPATH, "//a[@href='/sign-in']")
    assert button

    # After click -- should redirect to sign-up page
    button.click()
    assert driver.current_url == os.environ["FRONTEND"] + "/sign-in"

    # Wait page to load
    time.sleep(5)

    # Check if all 5 fields exist
    sign_in_fields_ids = [
        "email",
        "password",
    ]
    field_elements = [driver.find_element(By.ID, id_) for id_ in sign_in_fields_ids]
    assert all(field_elements)

    # Check if sign-in button exists
    sign_in_buttons = driver.find_elements(By.TAG_NAME, "button")
    for element in sign_in_buttons:
        if element.text == "Sign In":
            sign_in_button = element

    assert sign_in_button

    # Enter user data
    sign_in_data = {
        "email": temp_email,
        "password": "1234",
    }

    # Enter text to each field
    [
        el.send_keys(sign_in_data[key])
        for el, key in zip(field_elements, sign_in_data)
    ]

    # Wait until this button is clickable
    driver.execute_script("arguments[0].click();", sign_in_button)
    # Wait for an alert
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    # Wait page to load
    time.sleep(5)

    assert driver.current_url == os.environ["FRONTEND"] + "/account/info"

    # Wait page to load
    time.sleep(5)

    # Check if company button exists
    company_info_button = driver.find_element(By.LINK_TEXT, "Company info")
    assert company_info_button

    # Click on company edit button
    driver.execute_script("arguments[0].click();", company_info_button)
    # Should be redirected to company info page
    assert driver.current_url == os.environ["FRONTEND"] + "/account/company/info/company-name-inc"

    # Wait page to load
    time.sleep(5)

    # Check if edit button exists
    edit_button = driver.find_element(By.LINK_TEXT, "Edit")

    assert edit_button

    # Click on company edit button
    driver.execute_script("arguments[0].click();", edit_button)
    # Should be redirected to company edit page
    assert driver.current_url == os.environ["FRONTEND"] + "/account/company/edit/company-name-inc"

    # Wait page to load
    time.sleep(5)

    # Set up all fields and click edit
    company_data = {
        "website": "website.com",
        "company_name": "company name inc",
        "jurisdiction": "Georgia, USA"
    }
    field_elements = [driver.find_element(By.ID, id_) for id_ in company_data]
    assert all(field_elements)

    # Check if edit button exists
    edit_buttons = driver.find_elements(By.TAG_NAME, "button")
    for element in edit_buttons:
        if element.text == "Edit":
            edit_button = element

    assert edit_button

    # Enter text to each field
    [
        el.send_keys(company_data[key])
        for el, key in zip(field_elements, company_data)
    ]

    # Click on company edit button
    driver.execute_script("arguments[0].click();", edit_button)
    # Wait for an alert
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    # If editting was successful, then redirect
    assert driver.current_url == os.environ["FRONTEND"] + "/account/info"
