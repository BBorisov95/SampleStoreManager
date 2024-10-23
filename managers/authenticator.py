from datetime import datetime, timedelta

import jwt
import werkzeug.exceptions
from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt.exceptions import DecodeError
from werkzeug.exceptions import Unauthorized, BadRequest

from db import db
from models import UserModel


class AuthenticatorManager:

    @staticmethod
    def encode_token(user):
        payload_data = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(days=30), # TODO ONLY FOR TESTING!
            "role": user.role if isinstance(user.role, str) else user.role.name,
        }
        token = jwt.encode(
            payload=payload_data, key=config("secret_key"), algorithm="HS256"
        )
        return token

    @staticmethod
    def decode_token(token):
        try:
            token_info = jwt.decode(
                jwt=token, key=config("secret_key"), algorithms=["HS256"]
            )
            return token_info.get("sub"), token_info.get("role")
        except DecodeError as de:
            """
            if Empty token or wrong token
            """
            raise BadRequest("Invalid credentials!")
        except Exception as e:
            # TODO do not raise general exception
            raise e


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    try:
        user_id, user_type = AuthenticatorManager.decode_token(token)
        return db.session.execute(db.select(UserModel).filter_by(id=user_id)).scalar()
    except werkzeug.exceptions.Unauthorized:
        raise Unauthorized("Wrong token provided!")
