from marshmallow import Schema, fields


class AllowedCountriesResponseSchema(Schema):
    allowed_countries_to_deliver = fields.Dict(keys=fields.String, values=fields.String)
