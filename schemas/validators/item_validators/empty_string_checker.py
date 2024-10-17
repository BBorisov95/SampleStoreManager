from marshmallow import ValidationError


def is_empty_string(value: str, check_field: str):
    if not value.strip():
        raise ValidationError(f"{check_field} cannot be empty string value!")
