# Copyright 2023 Free World Certified -- all rights reserved.
"""Contains the pm tests."""
import os
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.utils import get_emails


def test_product_manager_create_and_edit(
    driver: webdriver.Chrome,
    signed_in_client: dict,
):

    driver.get(os.environ["FRONTEND"] + "/account/pm")
    assert driver.current_url == os.environ["FRONTEND"] + "/account/pm"

    # Enter user data
    create_pm_data = {
        "email": "pm@website.com",
        "password": "4321",
        "first_name": "Bob",
        "last_name": "Jackson",
    }

    field_elements = [driver.find_element(By.ID, id_) for id_ in create_pm_data.keys()]
    assert all(field_elements)

    create_pm_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Create PM')]")),
    )

    # Enter text to each field
    [
        el.send_keys(create_pm_data[key])
        for el, key in zip(field_elements, create_pm_data)
    ]

    create_pm_button.click()

    # Wait for an alert & ensure PM account creation worked
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Successfully created"
    alert.accept()

    driver.get(os.environ["FRONTEND"] + "/account/pm")  # KJB: should not be need
    assert driver.current_url == os.environ["FRONTEND"] + "/account/pm"
    pm_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//a[@href='/account/pm/info/{create_pm_data['email']}']"),
        ),
    )
    assert pm_button

    pm_button.click()

    ############################################################
    # edit pm

    edit_pm_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Edit')]")),
    )
    assert edit_pm_button
    edit_pm_button.click()

    assert driver.current_url \
        == os.environ["FRONTEND"] + f"/account/pm/edit/{create_pm_data['email']}"

    # Set up all fields and click edit
    pm_update_data = {
        "first_name": "Robert",
    }
    field_elements = [driver.find_element(By.ID, id_) for id_ in pm_update_data]
    assert all(field_elements)

    # Check if edit button exists
    edit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Edit')]")),
    )
    assert edit_button

    # Enter text to each field
    [
        el.send_keys(pm_update_data[key])
        for el, key in zip(field_elements, pm_update_data)
    ]

    # Click on pm edit button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(edit_button)).click()
    # Wait for an alert
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Successfully edited"
    alert.accept()

    # If editing was successful, then redirect
    assert driver.current_url == os.environ["FRONTEND"] + "/account/pm"

    # Go back to pm info and check the changes
    # Wait to load this element
    pm_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//a[@href='/account/pm/info/{create_pm_data['email']}']"),
        ),
    )
    assert pm_button

    pm_button.click()

    new_first_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//p[contains(., '{pm_update_data['first_name']}')]",
            ),
        ),
    )
    assert new_first_name.text == pm_update_data["first_name"]

    ############################################################
    # sign admin out

    menu_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//button[contains(., '{signed_in_client['email']}')]",
            ),
        ),
    )
    assert menu_button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(menu_button)).click()

    sign_out_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Sign Out')]")),
    )
    assert sign_out_button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(sign_out_button)).click()

    ############################################################
    # log pm in

    # Wait for email to get
    for _ in range(10):
        time.sleep(1)
        emails = get_emails("pm@website.com")

        # If there are messages in sendgird
        if len(emails) > 0:
            break

    # ensure everything is in the first email that we expect
    assert len(emails) > 0
    assert "content" in emails[0]
    assert len(emails[0]["content"]) > 0
    assert "value" in emails[0]["content"][0]

    text = emails[0]["content"][0]["value"]

    regex = re.compile("(/activated/[a-zA-Z]{0,4}/[0-9a-zA-Z_-]+)")
    link = os.environ["FRONTEND"] + regex.search(text).group(1)
    assert link

    driver.get(link)
    success_indication = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(., 'Successfully activated!')]")),
    )
    assert success_indication

    # Check if sign-in button exists
    # It should lead to /sign-in url
    button = driver.find_element(By.XPATH, "//a[@href='/sign-in']")
    assert button

    # After click -- should redirect to sign-up page
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button)).click()
    assert driver.current_url == os.environ["FRONTEND"] + "/sign-in"

    # Enter user data
    sign_in_data = {
        "email": "pm@website.com",
        "password": "4321",
    }

    field_elements = [driver.find_element(By.ID, id_) for id_ in sign_in_data.keys()]
    assert all(field_elements)

    # Enter text to each field
    [
        el.send_keys(sign_in_data[key])
        for el, key in zip(field_elements, sign_in_data)
    ]

    sign_in_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Sign In')]")),
    )
    assert sign_in_button

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(sign_in_button)).click()
    # Wait for an alert
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Successfully logged"
    alert.accept()
