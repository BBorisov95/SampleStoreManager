from marshmallow import fields

from schemas.base_item_schema import BaseItemSchema, BaseItemDetailSchema


class ItemResponseSchema(BaseItemDetailSchema):
    pass


class ItemResponseManagersSchema(BaseItemDetailSchema):

    id = fields.Integer(required=True)
    stocks = fields.Integer(required=True)
    sold_pieces = fields.Integer(required=True)


class ItemResponseDispatcherSchema(BaseItemSchema):
    id = fields.Integer(required=True)
