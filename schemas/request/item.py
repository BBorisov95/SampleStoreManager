from marshmallow import fields

from schemas.base_item_schema import BaseItemDetailSchema, BaseUpdateItemSchema
from schemas.validators.item_validators.stock_validator import validate_stock


class ItemCreationSchema(BaseItemDetailSchema):

    stocks = fields.Integer(required=True, validate=validate_stock)


class ItemUpdateSchema(BaseUpdateItemSchema):
    prod_id = fields.Integer(required=True)


class ItemRestockSchema(BaseUpdateItemSchema):
    prod_id = fields.Integer(required=True)
    stock = fields.Integer(required=True, validate=lambda x: x > 0)


class ItemListRestocksSchema(BaseUpdateItemSchema):
    items = fields.List(fields.Nested(ItemRestockSchema), required=True)
