from marshmallow import ValidationError
from pasword_validator import validate_password


def password_validator(func):
    def wrapper(*args, **kwargs):
        password = kwargs.get("password")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        if password is None:
            raise ValidationError("Password is required.")
        validate_password(password=password, fn=first_name, ln=last_name)
        return func(*args, **kwargs)

    return wrapper
