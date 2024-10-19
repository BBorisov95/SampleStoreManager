from marshmallow import Schema, fields

from schemas.base_order_address_schema import DeliveryAddressSchema


class OrderBuckedSchema(Schema):
    prod_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True, validate=lambda x: x > 0)


class OrderPlaceSchema(Schema):
    items = fields.List(fields.Nested(OrderBuckedSchema), required=True)
    delivery_address = fields.Nested(DeliveryAddressSchema, required=True)
