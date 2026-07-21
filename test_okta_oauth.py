from okta_oauth import get_access_token

import requests

from dotenv import load_dotenv

import os


load_dotenv()


OKTA_ORG_URL = os.getenv(
    "OKTA_ORG_URL"
)


access_token = get_access_token()


if not access_token:

    print(
        "Could not obtain access token"
    )

    exit()


headers = {

    "Authorization":
        f"Bearer {access_token}",

    "Accept":
        "application/json"

}


url = (

    f"{OKTA_ORG_URL}"

    "/api/v1/users"

)


response = requests.get(

    url,

    headers=headers,

    timeout=30

)


print(

    "Status code:",

    response.status_code

)


print(

    response.text

)
