from marshmallow import ValidationError


def validate_stock(stock: int):

    if not isinstance(stock, int):
        raise ValidationError(f"Stock value must be integer got {type(stock)}")

    if stock < 0:
        raise ValidationError("Stock cannot go to negative number!")
