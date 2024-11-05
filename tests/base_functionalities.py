from flask_testing import TestCase

from config import TestingConfig
from config import create_app
from db import db
from managers.authenticator import AuthenticatorManager
from models import UserModel


def generate_token(user):
    return AuthenticatorManager.encode_token(user)


class APIBaseTestCase(TestCase):
    """
    Base class which handles the common commands for tests
    """

    def create_app(self):
        """
        Create a test instance
        :return: app instance with test env
        """
        return create_app(TestingConfig)

    def setUp(self):
        """
        Build clean test db!
        """
        db.create_all()

    def tearDown(self):
        """
        Drop all testing dbs.
        :return:
        """
        db.session.remove()
        db.drop_all()

    def register_user(self) -> tuple[str, str]:
        """
        Base method to return mail,pass and
        trigger user registration.
        :return: tuple(mail, pass)
        """
        data: dict = {
            "username": "ValidUserName",
            "password": "Valid@$$w0rd",
            "first_name": "FirstName",
            "last_name": "LastName",
            "email": "fname@lname.com",
        }

        users: list[UserModel] = UserModel.query.all()
        self.assertEqual(len(users), 0)  # initial state

        resp = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 201)
        token: str = resp.json["token"]
        self.assertIsNotNone(token)  # check if token is indeed returned
        return data["username"], data["password"]
