from marshmallow import Schema, fields

from utils.validators.price_validator import validate_price


class BaseItemSchema(Schema):
    name = fields.String(required=True)
    price = fields.Float(required=True, validate=validate_price)
    part_number = fields.String(required=True)
    ean = fields.Float(required=True)
    category = fields.String(required=True)
    specs = fields.Dict()
