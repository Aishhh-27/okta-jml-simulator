from okta_oauth import get_access_token


access_token = get_access_token()


if access_token:

    print(
        "OAuth token received successfully"
    )

    print(
        "Token length:",
        len(access_token)
    )

else:

    print(
        "Failed to obtain OAuth token"
    )
