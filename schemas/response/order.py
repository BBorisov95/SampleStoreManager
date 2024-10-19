from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.enums import OrderStatus, DeliveryType, PaymentStatus
from schemas.base_order_address_schema import DeliveryAddressSchema


class OrderResponseSchema(Schema):

    id = fields.Integer()
    delivery_to = fields.Nested(DeliveryAddressSchema)
    status = EnumField(OrderStatus, by_value=True)
    delivery_type = EnumField(DeliveryType, by_value=True)
    payment_status = EnumField(PaymentStatus, by_value=True)
    total_order = fields.Float()
