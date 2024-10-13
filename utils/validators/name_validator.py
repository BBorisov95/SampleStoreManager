from marshmallow.schema import ValidationError


def validate_name(name: str):
    """
    Validate names
    :param name: first/last name
    :return: Rises if error
    """
    if not name.isalpha():
        raise ValidationError("Name must only contain alphabetic characters.")
    if len(name) < 2 or len(name) > 20:
        raise ValidationError("Name must be between 2 and 20 characters.")