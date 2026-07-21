from okta_client import get_okta_users


response = get_okta_users()


print(
    "Status code:",
    response.status_code
)


print(
    "Response:"
)


print(
    response.text
)
