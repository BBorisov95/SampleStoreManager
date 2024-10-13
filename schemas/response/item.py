from marshmallow import fields

from schemas.base_item_schema import BaseItemSchema


class ItemResponseSchema(BaseItemSchema):

    name = fields.String(required=True)
    price = fields.Float(required=True)
    part_number = fields.String(required=True)
    ean = fields.Float(required=True)
    category = fields.String(required=True)
    specs = fields.Dict()
