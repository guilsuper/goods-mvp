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
from sendgrid.helpers.mail import Mail

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
    """

    sendgrid_host = os.environ.get("SENDGRID_HOST", None)
    if sendgrid_host:
        sg = SendGridAPIClient(host=sendgrid_host)
    else:
        sg = SendGridAPIClient()
        sendgrid_host = "<sendgrid-default>"  # only used for logging below

    admin = Administrator.objects.get(id=user_id)

    subject = "Activate your account."
    message = render_to_string(
        "template_activate_account.html",
        {
            "frontend_url": os.environ["FRONTEND_HOST"],
            "uid": urlsafe_base64_encode(force_bytes(admin.pk)),
            "token": account_activation_token.make_token(admin),
        }
    )

    mail = Mail(
        from_email='support@freeworldcertified.org',
        to_emails=[admin.email],
        subject=subject,
        html_content=message)

    try:
        response = sg.send(mail)

        if response.status_code >= 200 and response.status_code < 300:
            logger.info("Sent email via %s to %s return code %d",
                        sendgrid_host, admin.email, response.status_code)
            return True
        else:
            logger.warning("Failed to send email via %s to %s return code %d info '%s'",
                           sendgrid_host, admin.email, response.status_code, response.body)
            return False

    except Exception as e:
        logger.warning("Failed to send email via %s to %s with error '%s'",
                       sendgrid_host,
                       admin.email,
                       e)
        return False
