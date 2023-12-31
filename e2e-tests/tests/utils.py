# Copyright 2023 Free World Certified -- all rights reserved.
import os
import re
import time

import numpy
import requests
from PIL import Image


def get_emails(email: str) -> list():
    """Gets emails for the user specified by email from mock sendgrid server

    Args:
        email: email of the users email to be fetched
    Returns:
        list of emails the user has received

        [{'datetime': '2023-08-23T20:27:57.538Z',
          'from': {'email': 'support@freeworldcertified.org'},
          'subject': 'Activate your account.',
          'personalizations': [{'to': [{'email': 'ken@ken.fwc'}]}],
          'content': [{'type': 'text/html',
          'value':
          '\nGreetings,\n\nPlease follow this link to activate your account:
                        \n\nhttp://localhost:3000/activated/MTE/btejil-55f6d689f8a1f67d0a325033288b06e9\n\n'}]}]
    """

    sendgrid_host = os.environ["SENDGRID_HOST"]
    result = requests.get(f"{sendgrid_host}/api/mails?to={email}")
    result.raise_for_status()

    return result.json()


def init_client() -> dict:
    """Creates a user in the project and returns its info and initial tokens."""
    data = {
        "email": "nazar@gmail.com",
        "password": "1234",
        "website": "aaaa.com",
        "name": "aaaa",
        "jurisdiction": "bruh",
    }

    response = requests.post(
        os.environ["BACKEND"] + "/api/admin_and_company/create/",
        data=data,
    )
    response.raise_for_status()

    # Wait for email to get
    for _ in range(10):
        time.sleep(1)
        emails = get_emails(data["email"])

        # If there are messages in sendgird
        if len(emails) > 0:
            break

    text = emails[0]["content"][0]["value"]

    # Compiles activation link that can be used to make a request to the backend
    regex = re.compile("(/activated/[a-zA-Z]{0,4}/[0-9a-zA-Z_-]+)")
    link = os.environ["BACKEND"] + regex.search(text).group(1).replace(
        "/activated", "/api/activate",
    ) + "/"
    requests.get(link)

    response = requests.post(
        os.environ["BACKEND"] + "/api/token/",
        data={
            "email": data["email"],
            "password": data["password"],
        },
    )
    response.raise_for_status()
    tokens = response.json()

    # To get full user info and company info
    response = requests.get(
        os.environ["BACKEND"] + "/api/self/patch_delete_retrieve/",
        headers={"Authorization": f"Bearer {tokens['access']}"},
    )
    response.raise_for_status()
    user = response.json()
    user["tokens"] = tokens
    user["password"] = data["password"]

    return user


def update_client_info(client: dict) -> dict:
    """Is used to update _client's information after each test.

    The data in e2e tests is permanent in a single session.
    This function is used to manage _client's data after each test.
    """
    response = requests.get(
        os.environ["BACKEND"] + "/api/self/patch_delete_retrieve/",
        headers={"Authorization": f"Bearer {client['tokens']['access']}"},
    )
    response.raise_for_status()
    response = response.json()

    client.update(response)
    client["company"].update(response["company"])
    return client


def get_country_data() -> dict():
    response = requests.get(os.environ["BACKEND"] + "/api/country/list/")
    response.raise_for_status()
    country_list = response.json()
    country_map = {}
    for country in country_list:
        country_map[country["alpha_2"]] = country
    return country_map


def compare_images(img1: Image, img2: Image) -> float:
    """Compare 2 images if they are the same using MSE."""
    # MSE is a metric, if it close to 0, then 2 arrays (images) are similar
    # For more details:
    # https://pyimagesearch.com/2014/09/15/python-compare-two-images/
    return numpy.mean((numpy.array(img1) - numpy.array(img2)) ** 2)
