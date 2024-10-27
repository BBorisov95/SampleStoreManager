from marshmallow import Schema, fields


class CountryCreateAndUpdateSchema(Schema):
    country_name = fields.String(required=True)
    prefix = fields.String(required=True)
    regular_delivery_price = fields.Float(required=True, validate=lambda x: x >= 0)
    fast_delivery_price = fields.Float(required=True, validate=lambda x: x >= 0)
    express_delivery_price = fields.Float(required=True, validate=lambda x: x >= 0)
    currency = fields.String(required=True, validate=lambda x: 3 <= len(x) <= 5)
    last_update_by = fields.Integer(required=True)
