from okta_api import get_users


response = get_users()


print(
    "Status code:",
    response.status_code
)


print(
    response.text
)
