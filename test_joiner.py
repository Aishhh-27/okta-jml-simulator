from okta_api import create_user


user_data = {

    "profile": {

        "firstName":
            "John",

        "lastName":
            "Smith",

        "email":
            "john.smith@acmecloud.example",

        "login":
            "john.smith@acmecloud.example"

    }

}


response = create_user(

    user_data

)


print(

    "Status code:",

    response.status_code

)


print(
    "Response body:",
    response.text
)
