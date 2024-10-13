from marshmallow import Schema
from flask_restful import request
from werkzeug.exceptions import BadRequest


def validate_schema(schema_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            schema: Schema = schema_name()
            data = request.get_json()
            errors = schema.validate(data)
            if errors:
                raise BadRequest(f"Invalid payload {errors}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
