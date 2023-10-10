# Copyright 2023 Free World Certified -- all rights reserved.
"""Useful utils functions."""
import logging
import os

from api.models import Administrator
from api.tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import ClickTracking
from sendgrid.helpers.mail import From
from sendgrid.helpers.mail import HtmlContent
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import OpenTracking
from sendgrid.helpers.mail import PlainTextContent
from sendgrid.helpers.mail import Subject
from sendgrid.helpers.mail import SubscriptionTracking
from sendgrid.helpers.mail import To
from sendgrid.helpers.mail import TrackingSettings

logger = logging.getLogger(__name__)


def send_activation_email(user_id: int) -> bool:
    """Sends activation email to the user with id=user_id.

    Args:
        user_id: index of the user in the DB.

    Returns:
        boolean if email sent successfully

    Note:
        Extracts the send grid api key from the environment variable SENDGRID_API_KEY
        For testing the sendgrid host can be overridden with SENDGRID_HOST

    Upstream Documentation:
        https://docs.sendgrid.com/api-reference/mail-send/mail-send
    """

    try:

        sendgrid_host = os.environ.get("SENDGRID_HOST", None)
        if sendgrid_host:
            sg = SendGridAPIClient(host=sendgrid_host)
        else:
            sg = SendGridAPIClient()
            sendgrid_host = "<sendgrid-default>"  # only used for logging below

        admin = Administrator.objects.get(id=user_id)

        template_params = {
            "frontend_url": os.environ["FRONTEND_HOST"],
            "uid": urlsafe_base64_encode(force_bytes(admin.pk)),
            "token": account_activation_token.make_token(admin),
        }

        txt_message = render_to_string(
            "template_activate_account.txt",
            template_params,
        )
        html_message = render_to_string(
            "template_activate_account.html",
            template_params,
        )

        mail = Mail(
            from_email=From(
                email="support@freeworldcertified.org",
                name="Free World Certified Support",
            ),
            to_emails=To(admin.email),
            subject=Subject("Activate your account."),
            plain_text_content=PlainTextContent(txt_message),
            html_content=HtmlContent(html_message),
        )

        mail.tracking_settings = TrackingSettings(
            click_tracking=ClickTracking(
                enable=False,
                enable_text=False,
            ),
            open_tracking=OpenTracking(
                enable=False,
            ),
            subscription_tracking=SubscriptionTracking(False),
        )

        response = sg.send(mail)

        if response.status_code >= 200 and response.status_code < 300:
            logger.info(
                "Sent email via %s to %s return code %d",
                sendgrid_host, admin.email, response.status_code,
            )
            return True
        else:
            logger.warning(
                "Failed to send email via %s to %s return code %d info '%s'",
                sendgrid_host, admin.email, response.status_code, response.body,
            )
            return False

    except Exception as e:
        logger.warning(
            "Failed to send email via %s to %s with error '%s'",
            sendgrid_host,
            admin.email,
            e,
        )
        return False


def dict_to_form_data(data: dict, sep: str = "[{i}]") -> dict:
    """Converts dict data to multipart/form-data friendly dict.

    Args:
        data: raw python dictionary.
        sep: arrays separator (symbol to identify an array-like variable).

    Returns:
        Modified dictionary that supports multipart content-type.

    Examples:
        Converting the following dictionary:

        ```python
        data = {
            "name": "Abro",
            "status": {
                "code": "112",
                "desc": "why",
                "workers": [
                    {
                        "name": "1111"
                    }
                ]
            },
            "notes": ["1", "2"]
        }
        ```

        Using `dict_to_form_data(data)` results in the
        following multipart/form-data friendly dictionary:

        ```python
        {
            'name': 'Abro',
            'status.code': '112',
            'status.desc': 'why',
            'status.workers[0]name': '1111',
            'notes[0]': '1',
            'notes[1]': '2'
        }
        ```
    """
    def inner(input: dict, inner_sep: str, result: dict, previous=None) -> dict:
        """Inner function to transform data as a recursive function."""
        # If inner element is a dictionary
        if isinstance(input, dict):
            if previous == "dict":
                inner_sep += "."
            for key, value in input.items():
                inner(value, inner_sep + key, result, "dict")
        # If inner element is array-like
        elif isinstance(input, (list, tuple)):
            for index, value in enumerate(input):
                inner(value, inner_sep + sep.format(i=index), result)
        else:
            result[inner_sep] = input

        return result

    return inner(data, "", {})
