import json

from okta_api import (
    create_user,
    get_user_by_email,
    update_user,
    suspend_user
)


def process_joiner(event):

    employee = event["employee"]

    email = employee["email"]

    existing_users_response = get_user_by_email(email)

    if existing_users_response.status_code == 200:

        existing_users = existing_users_response.json()

        if existing_users:

            print(
                f"User already exists: {email}"
            )

            return

    user_data = {

        "profile": {

            "firstName":
                employee["first_name"],

            "lastName":
                employee["last_name"],

            "email":
                email,

            "login":
                email

        }

    }

    response = create_user(user_data)

    print(
        "Status code:",
        response.status_code
    )

    print(
        "Response body:",
        response.text
    )


def process_mover(event):

    employee = event["employee"]

    email = employee["email"]

    response = get_user_by_email(email)

    if response.status_code != 200:

        print(
            "Failed to find user:",
            response.text
        )

        return

    users = response.json()

    if not users:

        print(
            f"User not found: {email}"
        )

        return

    user = users[0]

    user_id = user["id"]

    update_data = {

        "profile": {

            "department":
                employee["department"],

            "title":
                employee["job_title"]

        }

    }

    update_response = update_user(

        user_id,

        update_data

    )

    print(
        "Status code:",
        update_response.status_code
    )

    print(
        "Response body:",
        update_response.text
    )


def process_leaver(event):

    employee = event["employee"]

    email = employee["email"]

    response = get_user_by_email(email)

    if response.status_code != 200:

        print(
            "Failed to find user:",
            response.text
        )

        return

    users = response.json()

    if not users:

        print(
            f"User not found: {email}"
        )

        return

    user = users[0]

    user_id = user["id"]

    suspend_response = suspend_user(user_id)

    print(
        "Status code:",
        suspend_response.status_code
    )

    print(
        "Response body:",
        suspend_response.text
    )


def process_event(event):

    event_type = event["event_type"]

    if event_type == "JOINER":

        process_joiner(event)

    elif event_type == "MOVER":

        process_mover(event)

    elif event_type == "LEAVER":

        process_leaver(event)

    else:

        print(
            "Unsupported event type:",
            event_type
        )


with open(
    "events/leaver.json",
    "r"
) as file:

    event = json.load(file)


process_event(event)
