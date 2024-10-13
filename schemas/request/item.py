
from marshmallow import fields

from schemas.base_item_schema import BaseItemSchema
from utils.validators.stock_validator import validate_stock


class ItemCreationSchema(BaseItemSchema):

    stocks = fields.Integer(required=True, validate=validate_stock)
