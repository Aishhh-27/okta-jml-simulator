import os
import requests
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# Read Okta configuration
OKTA_ORG_URL = os.getenv(
    "OKTA_ORG_URL"
)

OKTA_API_TOKEN = os.getenv(
    "OKTA_API_TOKEN"
)


# Validate configuration
if not OKTA_ORG_URL:

    raise ValueError(
        "OKTA_ORG_URL is not configured"
    )


if not OKTA_API_TOKEN:

    raise ValueError(
        "OKTA_API_TOKEN is not configured"
    )


# Headers for Okta API requests
headers = {

    "Authorization":
        f"SSWS {OKTA_API_TOKEN}",

    "Accept":
        "application/json",

    "Content-Type":
        "application/json"
}


def get_okta_users():

    url = (
        f"{OKTA_ORG_URL}"
        "/api/v1/users"
    )


    response = requests.get(

        url,

        headers=headers,

        timeout=30

    )


    return response
