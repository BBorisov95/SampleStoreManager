from marshmallow import fields

from schemas.base_item_schema import BaseItemSchema, BaseItemDetailSchema


class ItemResponseSchema(BaseItemDetailSchema):
    pass


class ItemResponseDispatcherSchema(BaseItemSchema):
    prod_id = fields.Integer(required=True)


class ItemResponseManagersSchema(ItemResponseDispatcherSchema):
    stocks = fields.Integer(required=True)
    sold_pieces = fields.Integer(required=True)
