from marshmallow import Schema, fields


class DispatchOrderRequestSchema(Schema):
    order_id = fields.Integer(required=True)
    last_update_by = fields.Integer(required=True)

