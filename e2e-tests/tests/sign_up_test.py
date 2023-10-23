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


def test_sign_up_correct(driver: webdriver.Chrome):
    """Check for a sign up flow."""
    driver.get(os.environ["FRONTEND"])

    # Healthcheck
    assert "Free World Certified" in driver.title

    # Check if sign-up button exists
    # It should lead to /sign-up url
    button = driver.find_element(By.XPATH, "//a[@href='/sign-up']")
    assert button

    # After click -- should redirect to sign-up page
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button)).click()

    assert driver.current_url == os.environ["FRONTEND"] + "/sign-up"

    # User user data
    sign_up_data = {
        "email": "admin@website.com",
        "password": "1234",
        "website": "website.com",
        "name": "company name inc",
        "jurisdiction": "Georgia, USA",
    }
    field_elements = [driver.find_element(By.ID, id_) for id_ in sign_up_data.keys()]
    assert all(field_elements)

    # Check if sign-up button exists
    sign_up_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Sign Up')]")),
    )
    assert sign_up_button

    # Enter text to each field
    [
        el.send_keys(sign_up_data[key])
        for el, key in zip(field_elements, sign_up_data)
    ]

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(sign_up_button)).click()

    # Wait for an alert & ensure account creation worked
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Successfully created. Check your email."
    alert.accept()

    # Wait for email to get
    for _ in range(10):
        time.sleep(1)
        emails = get_emails("admin@website.com")

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
        "email": "admin@website.com",
        "password": "1234",
    }

    field_elements = [driver.find_element(By.ID, id_) for id_ in sign_in_data.keys()]
    assert all(field_elements)

    sign_in_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Sign In')]")),
    )
    assert sign_in_button

    # Enter text to each field
    [
        el.send_keys(sign_in_data[key])
        for el, key in zip(field_elements, sign_in_data)
    ]

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(sign_in_button)).click()
    # Wait for an alert
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Successfully logged"
    alert.accept()

    assert driver.current_url == os.environ["FRONTEND"] + "/account/info"

    ############################################################
    # test company website edit

    company_info_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Company info")),
    )
    assert company_info_button

    # Click on company edit button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(company_info_button)).click()

    # Should be redirected to company info page
    assert driver.current_url == os.environ["FRONTEND"] + "/account/company/info/company-name-inc"

    # Check if edit button exists
    edit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Edit")),
    )
    assert edit_button

    # Click on company edit button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(edit_button)).click()

    # Should be redirected to company edit page
    assert driver.current_url == os.environ["FRONTEND"] + "/account/company/edit/company-name-inc"

    # Set up all fields and click edit
    company_update_data = {
        "website": "website1.com",
    }
    field_elements = [driver.find_element(By.ID, id_) for id_ in company_update_data]
    assert all(field_elements)

    # Check if edit button exists
    edit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Edit')]")),
    )
    assert edit_button

    # Enter text to each field
    [
        el.send_keys(company_update_data[key])
        for el, key in zip(field_elements, company_update_data)
    ]

    # Click on company edit button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(edit_button)).click()
    # Wait for an alert
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Successfully edited"
    alert.accept()

    # If editing was successful, then redirect
    assert driver.current_url == os.environ["FRONTEND"] + "/account/info"

    # Go back to company info and check the changes
    # Wait to load this element
    company_info_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Company info")),
    )
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(company_info_button)).click()

    assert driver.current_url == os.environ["FRONTEND"] + "/account/company/info/company-name-inc"

    new_website = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//p[contains(., '{company_update_data['website']}')]",
            ),
        ),
    )
    assert new_website.text == company_update_data["website"]

    ############################################################
    # test sign out
    menu_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//button[contains(., '{sign_in_data['email']}')]",
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

    sign_in_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Sign In')]")),
    )
    assert sign_in_button
