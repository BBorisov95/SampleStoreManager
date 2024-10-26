from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.enums import OrderStatus, DeliveryType
from schemas.base_order_address_schema import DeliveryAddressSchema


class DispatchOrderResponseSchema(Schema):
    id = fields.Integer()
    customer_id = fields.Integer()
    status = EnumField(OrderStatus, by_value=True)
    delivery_type = EnumField(DeliveryType, by_value=True)
    delivery_address = fields.Nested(DeliveryAddressSchema, required=True)
    dispatch_link = fields.String()  # Add the new field for the order link
    created_at = fields.DateTime()
