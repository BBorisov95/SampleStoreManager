from marshmallow import Schema, fields, validates_schema
from utils.validators.pasword_validator import validate_password
from utils.validators.name_validator import validate_name
from utils.validators.mail_validator import email_validator


class BaseUserSchema(Schema):
    first_name = fields.String(required=False, validate=validate_name)
    last_name = fields.String(required=False, validate=validate_name)
    username = fields.String(required=True)
    password = fields.String(required=True)


class UserLoginSchema(BaseUserSchema):
    password = fields.String(required=True, validate=validate_password)


class UserRegisterSchema(UserLoginSchema):

    email = fields.Email(required=True, validate=email_validator)

    @validates_schema
    def validate_password_custom(self, data, **kwargs):
        """
        Harder password verification for passwords upon registration
        :param data: request data
        :param kwargs: required from decorator
        :return: None
        """
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        validate_password(password=password, fn=first_name, ln=last_name)
