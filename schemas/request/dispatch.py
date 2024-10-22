from marshmallow import Schema, fields


class DispatchOrderRequestSchema(Schema):
    order_id = fields.Integer(required=True)
