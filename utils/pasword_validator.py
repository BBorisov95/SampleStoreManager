import re

from marshmallow import ValidationError


def validate_password(password, fn=None, ln=None):
    """
    Validate the password for register/login/change password
    :param password: user's password
    :param fn: users_first name
    :param ln: users_last name
    :return: True if valid else raises ValidationError
    """
    if not 5 <= len(password) <= 12:
        raise ValidationError("Password must be between 5 and 12 characters long.")

    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r"[0-9]", password):
        raise ValidationError("Password must contain at least one digit.")

    if not re.search(r"[\W_]", password):
        raise ValidationError("Password must contain at least one special character.")

    if re.search(r"\d{2,}", password):
        raise ValidationError("Password must not contain consecutive digits.")
    if fn and ln:
        fn = fn.lower()
        ln = ln.lower()
        """
        for register
        change password
        """
        if fn in password.lower() or ln in password.lower():
            raise ValidationError("Your names cannot be part of your Password!")

        first_name_char = fn[0]
        last_name_char = ln[0]

        if first_name_char and last_name_char:
            if (
                f"{first_name_char}{last_name_char}" in password.lower()
                or f"{last_name_char}{first_name_char}" in password.lower()
            ):
                raise ValidationError(
                    "Password must not contain initials of your name!."
                )

    return True
