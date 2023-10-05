# Copyright 2023 Free World Certified -- all rights reserved.
"""Checks language selector works on main page."""
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_language_selecter_page(
    driver: webdriver.Chrome,
    client: dict,
):
    """Checks if language selector works on main page.
    Selects English; Test text; Selects German; Tests text; Selects English again; Test text.
    """

    driver.get(os.environ["FRONTEND"])

    # Healthcheck
    assert "Free World Certified" in driver.title

    # open language selector
    language_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Language')]")),
    )
    assert language_button
    language_button.click()

    # select english
    english_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(., 'English')]")),
    )
    assert english_button
    english_button.click()

    # confirm that our mission link has english text
    our_mission_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/our_mission']")),
    )
    assert our_mission_link
    assert our_mission_link.text == "Our Mission"

    # select language menu; select german
    language_button.click()
    deutsch_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Deutsch')]")),
    )
    assert deutsch_button
    deutsch_button.click()

    # confirm that our mission link has german
    our_mission_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/our_mission']")),
    )
    assert our_mission_link
    assert our_mission_link.text == "Unsere Mission"

    # select language menu; select english
    language_button.click()
    english_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(., 'English')]")),
    )
    assert english_button
    english_button.click()

    # confirm that our mission link has english text again
    our_mission_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/our_mission']")),
    )
    assert our_mission_link
    assert our_mission_link.text == "Our Mission"
