# Copyright 2023 Free World Certified -- all rights reserved.
import os

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
