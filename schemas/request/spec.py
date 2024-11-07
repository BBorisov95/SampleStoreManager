from marshmallow import Schema, fields, EXCLUDE

from schemas.validators.item_validators.part_number_validator import (
    validate_part_number,
)


class SpecAddSchema(Schema):
    internal_prod_id = fields.Integer(required=True)
    brand = fields.String(required=True)
    product_code = fields.String(required=True, validate=validate_part_number)
    ean = fields.String()
    use_paid_account = fields.Tuple(
        required=True,
        tuple_fields=(fields.String, fields.String),
    )

    class Meta:
        """
        Exclude last_update_by for most of the cases
        """

        unknown = EXCLUDE
