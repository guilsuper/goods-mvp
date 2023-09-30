# Copyright 2023 Free World Certified -- all rights reserved.
"""Checks if the qrcode is displayed on the Origin Report page,and it
has embedded the correct link."""
import os
from typing import Callable

import cv2
import numpy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_flag_origin_report_info_page(
    driver: webdriver.Chrome,
    origin_report_create_published: Callable,
    client: dict
):
    """Checks if the qr code is displayed in the OriginReport page with the correct link."""
    origin_report = origin_report_create_published()

    driver.get(os.environ["FRONTEND"] + "/origin_report")

    origin_report_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//a[@href='/origin_report/{origin_report['id']}']")
        )
    )
    assert origin_report_item

    # After click on a listed OriginReport -- should redirect to OriginReport page
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(origin_report_item)).click()
    assert driver.current_url == os.environ["FRONTEND"] + f"/origin_report/{origin_report['id']}"

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
    assert os.environ["FRONTEND"] + f"/origin_report/{origin_report['id']}" == qrcode_url
