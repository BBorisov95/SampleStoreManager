from marshmallow import Schema, fields
from schemas.validators.order_validators.delivery_address_validator import (
    validate_country,
    validate_city,
    validate_postal_code,
)


class DeliveryAddressSchema(Schema):
    to_country = fields.String(required=True, validate=validate_country)
    to_city = fields.String(required=True, validate=validate_city)
    to_zipcode = fields.String(required=True, validate=validate_postal_code)
