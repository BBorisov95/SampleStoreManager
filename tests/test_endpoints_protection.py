import requests

from models import UserRole, UserModel
from tests.base_functionalities import generate_token, APIBaseTestCase
from tests.factories import UserFactory


class TestProtectedEndpoints(APIBaseTestCase):
    """
    General test which checks if the endpoints are correctly protected
    by required login and permissions.
    """

    login_required_endpoints: tuple[tuple[str, str]] = (
        # item related
        ("GET", "/item/get-item/1"),
        ("POST", "/management/item/create-item"),
        ("PUT", "/management/item/update-item"),
        ("DELETE", "/management/item/delete-item/1"),
        ("PUT", "/data-entry/item/update-item-spec"),
        ("PUT", "/management/items/restock"),
        ("GET", "/items/category/''"),
        # orders
        ("POST", "/item/purchase"),
        ("GET", "/get-orders"),
        # dispatcher
        ("POST", "/dispatcher/dispatch"),
        ("GET", "/dispatcher/get-orders"),
        ("PUT", "/dispatcher/approve-shipped/1"),
    )

    def make_multiple_users_access_check_endpoint(self, users: list, endpoints: tuple):
        for user in users:
            user_token: str = generate_token(user)
            headers: dict = {
                "Authorization": f"Bearer {user_token}",
                "Accept": "application/json",
            }
            for method, url in endpoints:
                resp = self.make_request(method, url, headers=headers)

                self.assertEqual(resp.status_code, 403)
                expected_message: dict = {
                    "message": "You do not have permissions to access this resource"
                }
                self.assertEqual(resp.json, expected_message)

    def make_request(self, method: str, url: str, headers=None) -> requests.Response:
        """
        Common method to run requests
        :param method: get/post/put
        :param url: expected endpoint
        :param headers: requests headers
        :return: response
        """
        resp: requests.Response

        if method == "GET":
            resp = self.client.get(url, headers=headers)
        elif method == "POST":
            resp = self.client.post(url, headers=headers)
        elif method == "PUT":
            resp = self.client.put(url, headers=headers)
        else:
            resp = self.client.delete(url, headers=headers)

        return resp

    def test_login_required_endpoints_missing_token(self):
        """
        Run test where no token is provided
        :return:
        """
        for method, url in self.login_required_endpoints:
            resp = self.make_request(method, url)

            self.assertEqual(resp.status_code, 401)
            expected_message = {"message": "Wrong token provided!"}
            self.assertEqual(resp.json, expected_message)

    def test_login_required_endpoints_invalid_token(self):
        """
        Test where invalid token is provided
        """
        headers: dict = {"Authorization": "Bearer invalid"}

        for method, url in self.login_required_endpoints:
            resp = self.make_request(method, url, headers=headers)

            self.assertEqual(resp.status_code, 401)
            expected_message: dict = {"message": "Wrong token provided!"}
            self.assertEqual(resp.json, expected_message)

    def test_permission_required_to_be_manager(self):
        """
        Tests endpoints where manager role is required
        but trying to access it with different roles
        """
        endpoints: tuple[tuple[str, str], ...] = (
            # items
            ("POST", "/management/item/create-item"),
            ("DELETE", "/management/item/delete-item/1"),
            ("PUT", "/management/item/update-item"),
            ("PUT", "/management/items/restock"),
            # country
            ("POST", "/management/create-country"),
            ("PUT", "/management/update-country-taxes"),
        )

        users: list[UserModel] = [
            UserFactory(),  # regular user by default
            UserFactory(role=UserRole.dispatcher),
            UserFactory(role=UserRole.data_entry),
            UserFactory(role=UserRole.admin),
        ]
        self.make_multiple_users_access_check_endpoint(users=users, endpoints=endpoints)

    def test_permission_required_to_be_dispatcher(self):
        """
        Tests endpoints where dispatcher role is required
        but trying to access it with different roles
        """
        endpoints: tuple[tuple[str, str], ...] = (
            # items
            ("GET", "/dispatcher/get-orders"),
            ("POST", "/dispatcher/dispatch"),
            ("PUT", "/dispatcher/approve-shipped/1"),
        )

        users: list[UserModel] = [
            UserFactory(),  # regular user by default
            UserFactory(role=UserRole.manager),
            UserFactory(role=UserRole.data_entry),
            UserFactory(role=UserRole.admin),
        ]

        self.make_multiple_users_access_check_endpoint(users=users, endpoints=endpoints)

    def test_permission_required_to_be_data_entry(self):
        """
        Tests endpoints where data_entry role is required
        but trying to access it with different roles
        """
        endpoints: tuple[tuple[str, str], ...] = (
            # items
            ("PUT", "/data-entry/item/update-item-spec"),
        )

        users: list[UserModel] = [
            UserFactory(),  # regular user by default
            UserFactory(role=UserRole.manager),
            UserFactory(role=UserRole.dispatcher),
            UserFactory(role=UserRole.admin),
        ]

        self.make_multiple_users_access_check_endpoint(users=users, endpoints=endpoints)
