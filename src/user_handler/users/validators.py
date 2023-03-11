import re

from users.exceptions import UserInvalidEmailException


def is_login_valid(email: str):
    """
    Returns True if the given string is a valid email address, False otherwise.
    """

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    match = re.match(pattern, email)

    if match is None:
        raise UserInvalidEmailException(f"{email} is not valid email address")
