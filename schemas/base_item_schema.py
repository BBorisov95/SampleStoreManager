from marshmallow import Schema, fields

from utils.validators.item_validators.item_names_validator import validate_item_name
from utils.validators.item_validators.part_number_validator import validate_part_number
from utils.validators.item_validators.price_validator import validate_price


class BaseItemSchema(Schema):
    name = fields.String(required=True, validate=validate_item_name)
    part_number = fields.String(required=True, validate=validate_part_number)
    ean = fields.String(required=True)


class BaseItemDetailSchema(BaseItemSchema):
    price = fields.Float(required=True, validate=validate_price)
    category = fields.String(required=True)
    specs = fields.Dict()
