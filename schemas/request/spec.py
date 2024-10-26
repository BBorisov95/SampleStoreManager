from marshmallow import Schema, fields

from schemas.validators.item_validators.part_number_validator import (
    validate_part_number,
)


class SpecAddSchema(Schema):
    internal_prod_id = fields.Integer(required=True)
    brand = fields.String(required=True)
    product_code = fields.String(required=True, validate=validate_part_number)
    ean = fields.String()
    use_paid_account = fields.Tuple((fields.String, fields.String))
