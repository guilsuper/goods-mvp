#!/usr/bin/env python
# Copyright 2023 Free World Certified -- all rights reserved.
import logging
import os

from google.cloud import secretmanager

logger = logging.getLogger(__name__)

NAME_PREFIX = "_GCP_SECRET_"


def access_secret_version(secret_name):
    '''from the google tutorial
    '''
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Access the secret version.
    response = client.access_secret_version(name=secret_name)

    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')


def main():
    '''Iterates over the environment. For names that start with
    NAME_PREFIX it looks up the gcp secret found at that name. If it
    finds a secret with that name it strips the NAME_PREFIX from the
    name and prints the name and value in a form that can then be
    sourced into the calling shell.

    Starting with an environment with the following variable set:
    _GCP_SECRET_SPECIAL_KEY=projects/1233456789012/secrets/my-password/latest

    Assuming the value of the secret projects/1233456789012/secrets/my-password.latest is:
    TESTING_PASSWORD

    This program will emit:
    SPECIAL_KEY="TESTING_PASSWORD"
    export SPECIAL_KEY

    To get these values into your current environment:
    ./secrets_to_environment.py > /tmp/environment.sh
    source /tmp/environment.sh
    '''

    print(f"# produced by {__file__}")
    for name, value in os.environ.items():
        if name.startswith(NAME_PREFIX):
            new_name = name.removeprefix(NAME_PREFIX)

            print("")
            print(f"# {name}:{value}")
            try:
                secret = access_secret_version(value)

                print(f"{new_name}=\"{secret}\"")
                print(f"export {new_name}")

            except Exception as e:
                logger.error(f"Failed to fetch {name}:{value} because [{e}]")
                print("# failed to fetch")


if __name__ == "__main__":
    main()
