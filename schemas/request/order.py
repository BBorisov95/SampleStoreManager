from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from schemas.base_order_address_schema import DeliveryAddressSchema

from models.enums import DeliveryType


class OrderBucketSchema(Schema):
    prod_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True, validate=lambda x: x > 0)


class OrderPlaceSchema(Schema):
    items = fields.List(fields.Nested(OrderBucketSchema), required=True)
    delivery_address = fields.Nested(DeliveryAddressSchema, required=True)
    delivery_type = EnumField(DeliveryType, required=True)
