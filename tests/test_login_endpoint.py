from tests.base_functionalities import APIBaseTestCase


class TestLogin(APIBaseTestCase):
    """
    General suit for testing registration schema failures
    """

    def setUp(self):
        """
        SetUP the app + extend register to ensure that
        for each test we have credentials for login
        """
        super().setUp()
        self.username, self.password = self.register_user()

    def test_login_with_missing_schema_fields(self):
        """
        Tests the login errors when no data is provided
        """
        data: dict = {}

        resp = self.client.post("/login", json=data)
        error_message = resp.json["message"]
        for field in ("username", "password"):
            self.assertIn(field, error_message)

    def test_login_invalid_username_not_valid(self):
        """
        Test the case where username is not valid
        """
        data: dict = {"username": "notvalid", "password": self.password}
        resp = self.client.post("/login", json=data)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json["message"], "Invalid Username or password!")

    def test_login_invalid_password_not_valid(self):
        """
        Test the case where password is not valid
        """
        data: dict = {"username": self.username, "password": "notvalidpass"}
        resp = self.client.post("/login", json=data)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json["message"], "Invalid Username or password!")

    def test_successfully_login(self):
        """
        Successfully login
        """
        data: dict = {"username": self.username, "password": self.password}
        resp = self.client.post("/login", json=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.json["token"])
