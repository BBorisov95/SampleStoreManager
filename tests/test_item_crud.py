from db import db
from models.enums import UserRole
from models.item import ItemModel
from models.user import UserModel
from tests.base_functionalities import generate_token, APIBaseTestCase
from tests.factories import UserFactory, ItemFactory


class TestItemCrudMethods(APIBaseTestCase):
    """
    Test Item CRUD methods
    """

    def setUp(self):
        super().setUp()
        self.user: UserModel = UserFactory(role=UserRole.manager)
        self.item: ItemModel = ItemFactory(id=1)  # force to be 1
        self.user_token: str = generate_token(self.user)
        self.headers: dict = {
            "Authorization": f"Bearer {self.user_token}",
            "Accept": "application/json",
        }

        self.base_data: dict = {
            "name": "Item1",
            "price": 25.12,  # not valid
            "part_number": "p7",
            "ean": "1234567891011",
            "category": "",
            "specs": {},
            "stocks": 2,
        }

    def make_item_create_request(self, expected_msg: str, data: dict or None = None):
        """
        Common method for making requests and test the output str
        :param expected_msg: string which is expected
        :return: string
        """
        resp = self.client.post(
            "/management/item/create-item",
            json=self.base_data if not data else data,
            headers=self.headers,
        )
        self.assertEqual(resp.json["message"], expected_msg)
        return resp.json["message"]

    def test_item_schema_missing_fields(self):
        """
        Test item creation without all required fields.
        """
        data: dict = {}

        resp = self.client.post(
            "/management/item/create-item", json=data, headers=self.headers
        )
        error_msg: str = resp.json["message"]
        for field in (
            "name",
            "price",
            "part_number",
            "ean",
            "category",
            "stock",
        ):
            self.assertIn(field, error_msg)
        self.assertEqual(resp.status_code, 400)

    def test_schema_item_create_validate_price_validator(self):
        """
        Validate item schema price_validator custom function
        """

        # too much digits after decimal point
        self.base_data["price"] = 123.123
        expected_msg = (
            "Invalid payload {'price': ['Price must have at most two decimal places!']}"
        )
        self.make_item_create_request(expected_msg)

        # negative price
        self.base_data["price"] = -10
        expected_msg = (
            "Invalid payload {'price': ['Item price must be positive number!']}"
        )
        self.make_item_create_request(expected_msg)

        # price to big
        self.base_data["price"] = 1_000_001
        expected_msg = "Invalid payload {'price': ['Incorrect price!']}"
        self.make_item_create_request(expected_msg)

    def test_item_create_schema_validate_if_string_is_empty(self):
        """
        Catches the cases where we can send empty:
        [part_number, name]
        """
        str_to_filed_mapper: dict[str, str] = {
            "Item Name": "name",
            "Part number": "part_number",
        }
        for expected_field in ["Item Name", "Part number"]:
            copy_of_data = self.base_data.copy()
            copy_of_data[str_to_filed_mapper[expected_field]] = ""
            expected_msg = f"Invalid payload {{'{str_to_filed_mapper[expected_field]}': ['{expected_field} cannot be empty string value!']}}"
            self.make_item_create_request(expected_msg, data=copy_of_data)

    def test_item_delete_invalid_item(self):
        """
        Test the deletion of invalid item id
        """
        for item_id in ["40", "0", "-1", None, "asd", "", "   "]:
            resp = self.client.delete(
                f"/management/item/delete-item/{item_id}", headers=self.headers
            )
            if item_id == "0":
                self.assertEqual(
                    resp.json["message"], "Item id cannot be Null or Zero!"
                )
                self.assertEqual(resp.status_code, 400)
            elif item_id == "40":
                expected_msg = "The item which you search is not existing!"
                self.assertEqual(resp.json["message"], expected_msg)
            else:
                # start treating the urls li .../delete-item/-1 as part of url building
                # must raise 404
                self.assertEqual(resp.status_code, 404)

    def test_get_item_manager_schema(self):
        """
        verify response schema for manager
        """
        resp = self.client.get("/item/get-item/1", headers=self.headers)
        visible_fields: list = resp.json["item"].keys()
        fields_to_view: list = [
            "stocks",
            "sold_pieces",
            "last_update_by",
            "price",
            "id",
            "ean",
            "part_number",
            "name",
        ]
        for field in visible_fields:
            self.assertIn(field, fields_to_view)
        self.assertEqual(resp.status_code, 200)

    def test_get_item_regular_schema(self):
        """
        verify response schema for regular user
        """
        user: UserModel = UserFactory()
        token: str = generate_token(user)
        self.headers["Authorization"] = f"Bearer {token}"
        resp = self.client.get("/item/get-item/1", headers=self.headers)
        visible_fields: list = resp.json["item"].keys()
        fields_to_view: list = [
            "price",
            "category",
            "specs",
            "name",
            "part_number",
            "ean",
        ]
        for field in visible_fields:
            self.assertIn(field, fields_to_view)
        self.assertEqual(resp.status_code, 200)

    def test_get_item_dispatcher_schema(self):
        """
        verify response schema for dispatcher
        """
        user: UserModel = UserFactory(role=UserRole.dispatcher)
        token: str = generate_token(user)
        self.headers["Authorization"] = f"Bearer {token}"
        resp = self.client.get("/item/get-item/1", headers=self.headers)
        visible_fields: list = resp.json["item"].keys()
        fields_to_view: list = [
            "id",
            "name",
            "part_number",
            "ean",
        ]
        for field in visible_fields:
            self.assertIn(field, fields_to_view)
        self.assertEqual(resp.status_code, 200)

    def test_get_items_from_category_many_true_response(self):
        """
        Test get items from category with many=true
        test only the status code
        the items themself are checked in individual test cases above
        """
        category: ItemModel = self.item.category
        resp = self.client.get(f"/items/category/{category}", headers=self.headers)
        self.assertEqual(resp.status_code, 200)

    def test_schema_update_item(self):
        """
        Test schema update by manager
        """
        update_fields_data: dict[str, any] = {"prod_id": 1, "part_number": "pt7"}
        initial_item_state: str = self.item.part_number
        resp = self.client.put(
            "/management/item/update-item",
            headers=self.headers,
            json=update_fields_data,
        )
        self.assertEqual(resp.status_code, 201)
        state_after_update: ItemModel = ItemModel.query.filter_by(id=1).scalar()
        db.session.refresh(
            state_after_update
        )  # refresh the state -> because tear down did not triggered yet!
        self.assertEqual(
            state_after_update.part_number, update_fields_data["part_number"]
        )
        self.assertNotEquals(initial_item_state, state_after_update.part_number)

    def test_add_spec_schema(self):
        """
        Test schema where DE team can update specks
        """
        data_to_add = {}
        # TODO MUST MOCK

    def test_item_restock_schema(self):
        """
        Test item.stocks level modification based on
        ItemListRestocksSchema
        """
        current_stock: int = self.item.stocks
        restock_data: dict[str, list[dict[str, int]]] = {
            "items": [{"prod_id": 1, "stock": 10}]
        }
        resp = self.client.put(
            "/management/items/restock", headers=self.headers, json=restock_data
        )
        expected_stock: int = current_stock + restock_data.get("items")[0].get("stock")
        stock_in_db: ItemModel = ItemModel.query.filter_by(
            id=1
        ).scalar()  # verify that it's actualy in db not only on instance
        self.assertEqual(stock_in_db.stocks, expected_stock)
        self.assertEqual(resp.status_code, 201)
