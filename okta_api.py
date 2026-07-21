import os
import requests

from dotenv import load_dotenv

from okta_oauth import get_access_token


load_dotenv()


OKTA_ORG_URL = os.getenv(
    "OKTA_ORG_URL"
)


def get_headers():

    access_token = get_access_token()

    if not access_token:

        raise Exception(
            "Could not obtain Okta access token"
        )

    return {

        "Authorization":
            f"Bearer {access_token}",

        "Accept":
            "application/json",

        "Content-Type":
            "application/json"

    }


def get_users():

    url = (
        f"{OKTA_ORG_URL}"
        "/api/v1/users"
    )


    return requests.get(

        url,

        headers=get_headers(),

        timeout=30

    )


def get_user_by_email(email):

    url = (
        f"{OKTA_ORG_URL}"
        "/api/v1/users"
    )


    params = {

        "search":
            f'profile.email eq "{email}"'

    }


    return requests.get(

        url,

        headers=get_headers(),

        params=params,

        timeout=30

    )


def create_user(user_data):

    url = (
        f"{OKTA_ORG_URL}"
        "/api/v1/users"
    )


    return requests.post(

        url,

        headers=get_headers(),

        json=user_data,

        timeout=30

    )

def update_user(user_id, user_data):

    url = (
        f"{OKTA_ORG_URL}"
        f"/api/v1/users/{user_id}"
    )

    return requests.post(

        url,

        headers=get_headers(),

        json=user_data,

        timeout=30

    )
def suspend_user(user_id):

    url = (
        f"{OKTA_ORG_URL}"
        f"/api/v1/users/{user_id}/lifecycle/suspend"
    )

    return requests.post(

        url,

        headers=get_headers(),

        timeout=30

    )
