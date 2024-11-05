from flask_testing import TestCase

from config import TestingConfig
from config import create_app
from db import db
from managers.authenticator import AuthenticatorManager
from models import UserModel, UserRole, CountryModel, ItemModel
from tests.factories import UserFactory, CountryFactory


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

    def create_item(self) -> list[ItemModel]:
        """
        Base method to return mail,pass and
        trigger user registration.
        :return: list[ItemModel]
        """
        data: dict = {
            "name": "Item1",
            "price": 25.19,
            "part_number": "p7",
            "ean": "1234567891011",
            "category": "",
            "specs": {},
            "stocks": 2,
        }

        items: list[ItemModel] = ItemModel.query.all()
        self.assertEqual(len(items), 0)  # initial state

        resp = self.client.post("/management/item/create-item", json=data)
        self.assertEqual(resp.status_code, 201)
        items: list[ItemModel] = ItemModel.query.all()
        self.assertEqual(len(items), 1)
        return items

    @staticmethod
    def return_user_headers(for_role: UserRole):
        """
        Return header for requested user role
        :return:
        """
        user: UserModel = UserFactory(role=for_role)
        token = generate_token(user)
        headers: dict = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        return headers

    @staticmethod
    def create_countries(country_name: str, country_code: str) -> CountryModel:
        """
        Invoke country factory whenever is needed
        Create User with role Manager in order to create the country instance
        :return: country instance
        """
        country: CountryModel = CountryFactory(
            country_name=country_name, prefix=country_code
        )
        return country
