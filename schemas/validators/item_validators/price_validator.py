from marshmallow import ValidationError


def validate_price(price: float):

    if round(price, 2) != price:
        raise ValidationError("Price must have at most two decimal places!")
    if not isinstance(price, (int, float)):
        raise ValidationError(f"Invalid price type. Expected float got {type(price)}!")
    if price <= 0:
        raise ValidationError(f"Item price must be positive number!")
    if price > 1_000_000:
        raise ValidationError(f"Incorrect price!")
