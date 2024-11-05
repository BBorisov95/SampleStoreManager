import requests

from models import UserModel
from tests.base_functionalities import APIBaseTestCase


class TestRegister(APIBaseTestCase):
    """
    General suit for testing registration schema failures
    """

    def make_register_request(self, data: dict) -> requests.Response:
        resp: requests.Response = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 400)
        return resp

    def test_register_schema_missing_fields(self):
        """
        Test if any of the required register filed is missing
        """
        data: dict = {}

        users: list[UserModel] = UserModel.query.all()
        self.assertEqual(len(users), 0)  # initial check to ensure that the DB is clean

        resp = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 400)
        error_message: str = resp.json["message"]  # get the full smg
        for field in ("username", "password", "email"):
            """
            Check if fields in the tuple are in the error msg.
            """
            self.assertIn(field, error_message)

        users: list[UserModel] = UserModel.query.all()
        self.assertEqual(len(users), 0)  # ensure -> no records added

    def test_register_schema_invalid_email(self):
        """
        Test case for register schema -> invalid email
        """
        data = {
            "username": "TestUser",
            "email": "testUser",  # This is invalid value
            "password": "Valid@$$w0rd",  # invalid
        }

        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

        resp = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 400)
        error_message = resp.json["message"]
        expected_message = "Invalid payload {'email': ['Not a valid email address.', 'Invalid email address.']}"
        self.assertEqual(error_message, expected_message)
        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

    def test_register_schema_invalid_password(self):
        """
        Test custom password validations
        """
        data = {"username": "TestUser", "email": "a@a.com", "password": "Low"}

        # test short pass
        self.make_register_request(data)

        # test long pass
        data["password"] = "ThisPasswordIsToLong"
        self.make_register_request(data)

        # test upper char missing
        data["password"] = "notgoodpass"
        self.make_register_request(data)

        # test lower char missing
        data["password"] = "NOTGOODPASS"
        self.make_register_request(data)

        # test digit char missing
        data["password"] = "NotGoodPass"
        self.make_register_request(data)

        # test special char missing
        data["password"] = "N0tGoodPass"
        self.make_register_request(data)

        # test consecutive digit fail
        data["password"] = "NotG00dPa$$"
        self.make_register_request(data)

        # test name not in password
        data["first_name"] = "Test"
        data["last_name"] = "User"
        data["password"] = "TestUser0!"
        self.make_register_request(data)

        # test initial not in password
        data["first_name"] = "Test"
        data["last_name"] = "User"
        data["password"] = "TUpas0!"
        self.make_register_request(data)

        data["first_name"] = "Test"
        data["last_name"] = "User"
        data["password"] = "UTser0!"  # reverse initials
        self.make_register_request(data)

    def test_register_schema_email_validator(self):
        """
        Test email regex for failures
        """
        invalid_mails: list[str] = [
            "username@example..com",  # consecutive dots in domain
            "username@-example.com",  # domain starts with a hyphen
            "username@example-.com",  # domain ends with a hyphen
            "username@example.c",  # single character top level domains
            "user@exa_mple.com",  # underscore in domain name
            "username@example.123",  # numeric-only top level domains
            "username@.example.com",  # domain starts with dot
            "user name@example.com",  # spaces in email address
            "user@name@example.com",  # multiple @ symbols
            "'    '@example.com",  # spaces string user
            "''@example.com",  # empty string user
            "user@.example.com",  # domain starts with dot
            "user@example..com",  # multiple consecutive dots
            None,  # None type
        ]

        data: dict = {
            "username": "ValidUserName",
            "password": "Valid@$$w0rd",
            "first_name": "FirstName",
            "last_name": "LastName",
        }
        for invalid_mail in invalid_mails:
            data["email"] = invalid_mail
            resp = self.client.post("/register", json=data)
            self.assertEqual(resp.status_code, 400)

    def test_register(self):
        """
        Successful register attempts
        """
        self.register_user()

        users: list[UserModel] = UserModel.query.all()
        self.assertEqual(len(users), 1)
