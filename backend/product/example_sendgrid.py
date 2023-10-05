#!/bin/env python3
# Copyright 2023 Free World Certified -- all rights reserved.
"""Example that illustrates

1) using Google Secret Manager from python

2) using SendGrid to send an email from support@freeworldcertified.org

To use this in local development, you must run

     gcloud auth application-default login

which you can read about here:
https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev

and to run this (or something like it) in GKE, then this:

https://cloud.google.com/docs/authentication/provide-credentials-adc#containerized

and this:

https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity

"""
# using SendGrid"s Python Library
# https://github.com/sendgrid/sendgrid-python
# import os
from google.cloud import secretmanager
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# using GCP"s Secret Manager
# https://codelabs.developers.google.com/codelabs/secret-manager-python#5

PROJECT_ID = "fwc-website-394712"


def access_secret_version(secret_id, version_id="latest"):
    """from the google tutorial

    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode("UTF-8")


def send_email(subject, body, to_emails):

    message = Mail(
        from_email="support@freeworldcertified.org",
        to_emails=to_emails,
        subject=subject,
        html_content=body,
    )

    sendgrid_api_token = access_secret_version("sendgrid_token")
    sg = SendGridAPIClient(sendgrid_api_token)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)


if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("to_emails")
    parser.add_argument("--subject", default="Can you hear me now?")
    parser.add_argument("--body", default="Wow.")
    args = parser.parse_args()

    send_email(
        args.subject,
        f"<strong>{args.body}</strong>",
        args.to_emails,
    )
