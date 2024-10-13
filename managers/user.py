from werkzeug.exceptions import Unauthorized
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.authenticator import AuthenticatorManager
from models import UserModel
from utils.db_handler import do_commit


class UserManager:
    """
    Handle the UserModel related options
    """

    @staticmethod
    def create_user(user_data):
        user_data["password"] = generate_password_hash(
            user_data["password"], method="pbkdf2:sha256"
        )
        user = UserModel(**user_data)
        do_commit(user)
        return AuthenticatorManager.encode_token(user)

    @staticmethod
    def login(data):
        user = db.session.execute(
            db.select(UserModel).filter_by(username=data.get("username"))
        ).scalar()
        if user and check_password_hash(user.password, data.get("password")):
            return AuthenticatorManager.encode_token(user)
        raise Unauthorized("Invalid Username or password!")
