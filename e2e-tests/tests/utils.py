# Copyright 2023 Free World Certified -- all rights reserved.
import os
import re
import time

import requests


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
        "jurisdiction": "bruh"
    }
    user = requests.post(
        os.environ["BACKEND"] + "/api/admin_and_company/create/",
        data=data
    ).json()

    # Wait for email to get
    for _ in range(10):
        time.sleep(1)
        emails = get_emails(user["email"])

        # If there are messages in sendgird
        if len(emails) > 0:
            break

    text = emails[0]["content"][0]["value"]

    # Compiles activation link that can be used to make a request to the backend
    regex = re.compile("(/activated/[a-zA-Z]{0,4}/[0-9a-zA-Z_-]+)")
    link = os.environ["BACKEND"] + regex.search(text).group(1).replace(
        "/activated", "/api/activate"
    ) + "/"
    requests.get(link)

    user["tokens"] = requests.post(
        os.environ["BACKEND"] + "/api/token/",
        data={
            "email": data["email"],
            "password": data["password"]
        }
    ).json()
    return user
