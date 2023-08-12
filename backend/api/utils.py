# Copyright 2023 Free World Certified -- all rights reserved.
"""Useful utils functions."""
import os

from api.models import Administrator
from api.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_activation_email(user_id: int) -> bool:
    """Sends activation email to the user with id=user_id.

    Args:
        user_id: index of the user in the DB.

    Returns:
        boolean if email sent successfully
    """
    admin = Administrator.objects.get(id=user_id)

    mail_subject = "Activate your account."
    message = render_to_string(
        "template_activate_account.html",
        {
            "frontend_url": os.environ["FRONTEND_HOST"],
            "uid": urlsafe_base64_encode(force_bytes(admin.pk)),
            "token": account_activation_token.make_token(admin),
        }
    )

    email = EmailMessage(mail_subject, message, to=[admin.email])
    return email.send()
