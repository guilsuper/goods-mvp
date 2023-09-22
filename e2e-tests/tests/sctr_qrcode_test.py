# Copyright 2023 Free World Certified -- all rights reserved.
"""Checks if the qrcode is displayed on the SCTR page, and it has embedded the correct link."""
import os
from typing import Callable

import cv2
import numpy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_flag_sctr_info_page(
    driver: webdriver.Chrome,
    sctr_create_published: Callable,
    client: dict
):
    """Checks if the qr code is displayed in the SCTR page with the correct link."""
    sctr = sctr_create_published()

    driver.get(os.environ["FRONTEND"] + "/sctr")

    sctr_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//a[@href='/sctr/{sctr['id']}']"))
    )
    assert sctr_item

    # After click on a listed SCTR -- should redirect to SCTR page
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(sctr_item)).click()
    assert driver.current_url == os.environ["FRONTEND"] + f"/sctr/{sctr['id']}"

    # ensure that the QR Code is present
    qrcode_present = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[local-name()='svg']"))
    )
    assert qrcode_present

    # extract the QR Code image
    qrcode_image = driver.find_element(By.XPATH, "//*[local-name()='svg']")
    assert qrcode_image

    nparr = numpy.frombuffer(qrcode_image.screenshot_as_png, numpy.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()

    qrcode_url, bbox, straight_qrcode = detector.detectAndDecode(img)

    # ensure extracted url matches expected url
    assert os.environ["FRONTEND"] + f"/sctr/{sctr['id']}" == qrcode_url
