import os
import json
import time
import uuid

import jwt
import requests

from dotenv import load_dotenv
from jwt.algorithms import RSAAlgorithm


load_dotenv()


OKTA_ORG_URL = os.getenv("OKTA_ORG_URL")
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID")
OKTA_PRIVATE_KEY_PATH = os.getenv(
    "OKTA_PRIVATE_KEY_PATH"
)


if not OKTA_ORG_URL:
    raise ValueError(
        "OKTA_ORG_URL is not configured"
    )


if not OKTA_CLIENT_ID:
    raise ValueError(
        "OKTA_CLIENT_ID is not configured"
    )


if not OKTA_PRIVATE_KEY_PATH:
    raise ValueError(
        "OKTA_PRIVATE_KEY_PATH is not configured"
    )


with open(
    OKTA_PRIVATE_KEY_PATH,
    "r"
) as file:

    private_key_jwk = json.load(file)


private_key = RSAAlgorithm.from_jwk(
    json.dumps(private_key_jwk)
)


def get_access_token():

    now = int(time.time())


    jwt_payload = {
        "iss": OKTA_CLIENT_ID,
        "sub": OKTA_CLIENT_ID,
        "aud": (
            f"{OKTA_ORG_URL}"
            "/oauth2/v1/token"
        ),
        "iat": now,
        "exp": now + 300,
        "jti": str(uuid.uuid4())
    }


    client_assertion = jwt.encode(
        jwt_payload,
        private_key,
        algorithm="RS256",
        headers={
            "kid": private_key_jwk["kid"]
        }
    )


    print("JWT header and claims check:")
    print("Client ID:", OKTA_CLIENT_ID)
    print("KID:", private_key_jwk["kid"])
    print("Audience:", jwt_payload["aud"])
    print("Issuer:", jwt_payload["iss"])
    print("Subject:", jwt_payload["sub"])
    print("Algorithm: RS256")


    token_url = (
        f"{OKTA_ORG_URL}"
        "/oauth2/v1/token"
    )


    data = {
        "grant_type": "client_credentials",
        "scope": "okta.users.manage",
        "client_assertion_type":
            "urn:ietf:params:oauth:"
            "client-assertion-type:"
            "jwt-bearer",
        "client_assertion": client_assertion
    }


    response = requests.post(
        token_url,
        data=data,
        timeout=30
    )


    if response.status_code != 200:

        print(
            "Token request failed:"
        )

        print(
            "Status code:",
            response.status_code
        )

        print(
            response.text
        )

        return None


    token_data = response.json()


    return token_data["access_token"]
