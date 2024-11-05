from marshmallow import Schema, fields, EXCLUDE

from schemas.validators.item_validators.item_names_validator import validate_item_name
from schemas.validators.item_validators.part_number_validator import (
    validate_part_number,
)
from schemas.validators.item_validators.price_validator import validate_price


class BaseItemSchema(Schema):
    name = fields.String(required=True, validate=validate_item_name)
    part_number = fields.String(required=True, validate=validate_part_number)
    ean = fields.String(required=True)

    class Meta:
        """
        Exclude last_update_by for most of the cases
        """

        unknown = EXCLUDE


class BaseItemDetailSchema(BaseItemSchema):
    price = fields.Float(required=True, validate=validate_price)
    category = fields.String(required=True)
    specs = fields.Dict()


class BaseUpdateItemSchema(BaseItemSchema):
    name = fields.String(required=False, validate=validate_item_name)
    part_number = fields.String(required=False, validate=validate_part_number)
    ean = fields.String(required=False)
    price = fields.Float(required=False, validate=validate_price)
    category = fields.String(required=False)
    specs = fields.Dict()
    last_update_by = fields.Integer(required=True)
