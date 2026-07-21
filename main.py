import json
import argparse
from datetime import datetime


# -----------------------------
# JSON FILE FUNCTIONS
# -----------------------------

def load_json(file_path):

    try:

        with open(file_path, "r") as file:
            return json.load(file)

    except FileNotFoundError:

        print(
            "ERROR: File not found:",
            file_path
        )

        return None

    except json.JSONDecodeError:

        print(
            "ERROR: Invalid JSON:",
            file_path
        )

        return None


def save_json(file_path, data):

    with open(file_path, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )


# -----------------------------
# VALIDATION FUNCTIONS
# -----------------------------

def validate_event_fields(
    event,
    required_fields
):

    for field in required_fields:

        if field not in event:

            print(
                "ERROR: Missing field:",
                field
            )

            return False

    return True


def validate_department(
    department,
    access_policy
):

    if department not in access_policy:

        print(
            "ERROR: Unknown department:",
            department
        )

        return False

    return True


# -----------------------------
# AUDIT LOGGING
# -----------------------------

def write_audit_log(
    event_type,
    employee,
    action,
    result
):

    timestamp = datetime.now().isoformat()

    log_entry = (
        f"{timestamp} | "
        f"event={event_type} | "
        f"employee={employee} | "
        f"action={action} | "
        f"result={result}\n"
    )

    with open(
        "audit.log",
        "a"
    ) as file:

        file.write(
            log_entry
        )


# -----------------------------
# USER FUNCTIONS
# -----------------------------

def find_user(
    users,
    email
):

    for user in users:

        if user["email"] == email:

            return user

    return None


def create_user(
    users,
    event,
    required_access
):

    new_user = {

        "employee_id":
            event["employee_id"],

        "name":
            event["name"],

        "email":
            event["email"],

        "department":
            event["department"],

        "status":
            "active",

        "groups":
            required_access["groups"],

        "applications":
            required_access["applications"]
    }

    users.append(
        new_user
    )

    return new_user


# -----------------------------
# ACCESS RECONCILIATION
# -----------------------------

def calculate_access_changes(
    current_access,
    required_access
):

    current_groups = set(
        current_access["groups"]
    )

    required_groups = set(
        required_access["groups"]
    )

    current_applications = set(
        current_access["applications"]
    )

    required_applications = set(
        required_access["applications"]
    )

    return {

        "groups_to_remove":
            current_groups -
            required_groups,

        "groups_to_add":
            required_groups -
            current_groups,

        "groups_to_keep":
            current_groups &
            required_groups,

        "applications_to_remove":
            current_applications -
            required_applications,

        "applications_to_add":
            required_applications -
            current_applications,

        "applications_to_keep":
            current_applications &
            required_applications
    }


# -----------------------------
# JOINER WORKFLOW
# -----------------------------

def process_joiner(
    event,
    access_policy,
    users
):

    # Validate required fields

    if not validate_event_fields(

        event,

        [
            "employee_id",
            "name",
            "email",
            "department"
        ]

    ):

        return


    email = event["email"]


    # Check if user already exists

    existing_user = find_user(
        users,
        email
    )


    if existing_user:

        print(
            "User already exists:",
            email
        )

        return


    department = event[
        "department"
    ]


    # Validate department

    if not validate_department(

        department,
        access_policy

    ):

        return


    required_access = access_policy[
        department
    ]


    # Create the user

    new_user = create_user(

        users,
        event,
        required_access

    )


    print(
        "JOINER WORKFLOW"
    )

    print(
        "----------------"
    )

    print(
        "User created:",
        new_user["email"]
    )

    print(
        "Name:",
        new_user["name"]
    )

    print(
        "Department:",
        new_user["department"]
    )

    print(
        "Groups:",
        new_user["groups"]
    )

    print(
        "Applications:",
        new_user["applications"]
    )


    # Write audit log

    write_audit_log(

        "JOINER",

        new_user["email"],

        "User created and access assigned",

        "SUCCESS"

    )


# -----------------------------
# MOVER WORKFLOW
# -----------------------------

def process_mover(

    event,
    access_policy,
    users

):

    # Validate required fields

    if not validate_event_fields(

        event,

        [
            "employee_id",
            "name",
            "email",
            "old_department",
            "new_department"
        ]

    ):

        return


    email = event[
        "email"
    ]


    # Find the user

    user = find_user(

        users,
        email

    )


    if user is None:

        print(

            "User not found:",

            email

        )

        return


    old_department = event[
        "old_department"
    ]


    new_department = event[
        "new_department"
    ]


    # Validate both departments

    if not validate_department(

        old_department,
        access_policy

    ):

        return


    if not validate_department(

        new_department,
        access_policy

    ):

        return


    old_access = access_policy[
        old_department
    ]


    new_access = access_policy[
        new_department
    ]


    # Calculate access changes

    changes = calculate_access_changes(

        old_access,
        new_access

    )


    print(
        "MOVER WORKFLOW"
    )

    print(
        "--------------"
    )

    print(
        "Employee:",
        user["name"]
    )

    print(
        "Old department:",
        old_department
    )

    print(
        "New department:",
        new_department
    )


    print()


    print(
        "GROUP CHANGES"
    )

    print(

        "Remove:",

        changes[
            "groups_to_remove"
        ]

    )

    print(

        "Keep:",

        changes[
            "groups_to_keep"
        ]

    )

    print(

        "Add:",

        changes[
            "groups_to_add"
        ]

    )


    print()


    print(
        "APPLICATION CHANGES"
    )

    print(

        "Remove:",

        changes[
            "applications_to_remove"
        ]

    )

    print(

        "Keep:",

        changes[
            "applications_to_keep"
        ]

    )

    print(

        "Add:",

        changes[
            "applications_to_add"
        ]

    )


    # Update the user

    user["department"] = new_department

    user["groups"] = new_access[
        "groups"
    ]

    user["applications"] = new_access[
        "applications"
    ]


    # Write audit log

    write_audit_log(

        "MOVER",

        user["email"],

        "Department and access updated",

        "SUCCESS"

    )


# -----------------------------
# LEAVER WORKFLOW
# -----------------------------

def process_leaver(

    event,
    users

):

    # Validate required fields

    if not validate_event_fields(

        event,

        [
            "employee_id",
            "name",
            "email"
        ]

    ):

        return


    email = event[
        "email"
    ]


    # Find the user

    user = find_user(

        users,
        email

    )


    if user is None:

        print(

            "User not found:",

            email

        )

        return


    # Suspend the user

    user["status"] = (
        "suspended"
    )


    # Remove all groups

    user["groups"] = []


    # Remove all applications

    user["applications"] = []


    print(
        "LEAVER WORKFLOW"
    )

    print(
        "----------------"
    )

    print(

        "Employee:",

        user["name"]

    )

    print(
        "Status: suspended"
    )

    print(
        "All groups removed"
    )

    print(
        "All applications removed"
    )

    print(
        "Sessions should be revoked"
    )


    # Write audit log

    write_audit_log(

        "LEAVER",

        user["email"],

        "User suspended and all access removed",

        "SUCCESS"

    )

# -----------------------------
# MAIN PROGRAM
# -----------------------------

parser = argparse.ArgumentParser(
    description="Okta JML Workflow Simulator"
)


parser.add_argument(
    "--event-file",
    required=True,
    help="Path to the HR event JSON file"
)


args = parser.parse_args()


# Select the correct event file

event_file = args.event_file


# Load access policy

access_policy = load_json(
    "config/access_policy.json"
)


if access_policy is None:

    print(
        "Cannot continue without access policy."
    )

    exit()


# Load users database

users = load_json(
    "data/users.json"
)


if users is None:

    print(
        "Cannot continue without users database."
    )

    exit()


# Load selected event

event = load_json(
    event_file
)


if event is None:

    print(
        "Cannot continue without event."
    )

    exit()


# Get event type

event_type = event.get(
    "event_type"
)


# Route event to correct workflow

if event_type == "JOINER":

    process_joiner(
        event,
        access_policy,
        users
    )


elif event_type == "MOVER":

    process_mover(
        event,
        access_policy,
        users
    )


elif event_type == "LEAVER":

    process_leaver(
        event,
        users
    )


else:

    print(
        "ERROR: Unknown event type:",
        event_type
    )


# Save updated users database

save_json(

    "data/users.json",

    users

)
