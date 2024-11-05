from copy import deepcopy

from models.country import CountryModel
from models.enums import UserRole, OrderStatus
from models.item import ItemModel
from models.order import OrderModel
from tests.base_functionalities import APIBaseTestCase
from tests.factories import ItemFactory, OrderFactory, UserFactory


class TestOrders(APIBaseTestCase):
    """
    Test Suite for orders module
    """

    def setUp(self):
        super().setUp()
        self.headers: dict = self.return_user_headers(UserRole.regular)
        self.county: CountryModel = self.create_countries("Bulgaria", "BGN")
        self.valid_data = {
            "items": [{"prod_id": 1, "quantity": 2}],
            "delivery_address": {
                "to_country": "Bulgaria",
                "to_city": "Sofia",
                "to_zipcode": "BGR:1000",
                "to_street_address": "Opulchenska",
                "to_building_number": 6,
            },
            "delivery_type": "express",
        }

    def make_invalid_requests(self, data: dict, msg: str) -> None:
        resp = self.client.post("/item/purchase", json=data, headers=self.headers)
        self.assertEqual(resp.json["message"], msg)
        self.assert400(resp)

    def make_valid_request(
        self,
        data_to_use: dict,
        expected_total_order_cost: float,
        expected_payed_delivery: float,
        expected_orders_in_db: int,
    ) -> None:
        """
         Make valid requests to create different orders
        :param data_to_use: different payload
        :param expected_total_order_cost: order_cost based on product quantity * product price
        :param expected_payed_delivery: different cost for shipping based on country
        :param expected_orders_in_db: number of records in db after requests
        To access current order attributes we use -1 on expected_items_in_db -> because we use index of lists for this
        :return: None
        """
        order = self.client.post(
            "/item/purchase", headers=self.headers, json=data_to_use
        )
        orders: list[OrderModel] = OrderModel.query.all()
        self.assertEqual(len(orders), expected_orders_in_db)
        total_order: float = order.json["order"]["total_order"]
        self.assertEqual(total_order, expected_total_order_cost)
        payed_for_shipping: OrderModel = orders[
            expected_orders_in_db - 1
        ].payment_for_shipping  # -1 cuz of index w
        self.assertEqual(payed_for_shipping, expected_payed_delivery)

    def test_validate_order_bucket_schema_invalid_id_and_quantities(self):
        """
        Testing the OrderBucketSchema product
        where checking valid prod_id and quantities
        """

        # invalid prod_id
        invalid_prod_id_data = deepcopy(self.valid_data)
        invalid_prod_id_data["items"][0]["prod_id"] = "invalid"
        expected_msg = (
            "Invalid payload {'items': {0: {'prod_id': ['Not a valid integer.']}}}"
        )
        self.make_invalid_requests(data=invalid_prod_id_data, msg=expected_msg)

        # invalid quantity:
        invalid_prod_quantity = deepcopy(self.valid_data)
        invalid_prod_quantity["items"][0]["quantity"] = 0
        expected_msg = (
            "Invalid payload {'items': {0: {'prod_id': ['Not a valid integer.']}}}"
        )
        self.make_invalid_requests(data=invalid_prod_id_data, msg=expected_msg)

        invalid_prod_quantity["items"][0]["quantity"] = -1
        self.make_invalid_requests(data=invalid_prod_id_data, msg=expected_msg)

    def test_order_delivery_address_schema_invalid_delivery_address(self):
        """
        Test valid delivery address nested schema
        :return:
        """
        # invalid to_country
        invalid_to_country = deepcopy(self.valid_data)
        invalid_to_country["delivery_address"]["to_country"] = "Japan"
        expected_msg = (
            f"Sorry we cannot deliver your order to {invalid_to_country['delivery_address']['to_country']}."
            f" Currently we can deliver only to: {self.county.country_name}"
        )
        self.make_invalid_requests(invalid_to_country, expected_msg)

        # Empty City name
        invalid_to_city = deepcopy(self.valid_data)
        invalid_to_city["delivery_address"]["to_city"] = ""
        expected_msg = (
            "Invalid payload {'delivery_address': {'to_city': ['City cannot be empty "
            "string value!']}}"
        )
        self.make_invalid_requests(invalid_to_city, expected_msg)

        # missing to_street_address
        invalid_to_street_address = deepcopy(self.valid_data)
        del invalid_to_street_address["delivery_address"]["to_street_address"]
        expected_msg = (
            "Invalid payload {'delivery_address': {'to_street_address': ['Missing data "
            "for required field.']}}"
        )
        self.make_invalid_requests(invalid_to_street_address, expected_msg)

        # missing to_building_number
        invalid_to_building_number = deepcopy(self.valid_data)
        del invalid_to_building_number["delivery_address"]["to_building_number"]
        expected_msg = (
            "Invalid payload {'delivery_address': {'to_building_number': ['Missing data "
            "for required field.']}}"
        )
        self.make_invalid_requests(invalid_to_building_number, expected_msg)

        # validate bad zipcode
        invalid_to_zipcode = deepcopy(self.valid_data)
        del invalid_to_zipcode["delivery_address"]["to_zipcode"]
        expected_msg = (
            "Invalid payload {'delivery_address': {'to_zipcode': ['Missing data "
            "for required field.']}}"
        )
        self.make_invalid_requests(invalid_to_zipcode, expected_msg)

        # validate zipcode empty code
        invalid_to_zipcode = deepcopy(self.valid_data)
        invalid_to_zipcode["delivery_address"]["to_zipcode"] = ""
        expected_msg = (
            "Invalid payload {'delivery_address': {'to_zipcode': ['Postal Code cannot be empty "
            "string value!']}}"
        )
        self.make_invalid_requests(invalid_to_zipcode, expected_msg)

        # validate_postal_code validator valueError
        invalid_to_zipcode = deepcopy(self.valid_data)
        invalid_to_zipcode["delivery_address"]["to_zipcode"] = "BGR1000"
        expected_msg = (
            "Invalid postal code format. Required type is COUNTRY_PREFIX:POSTAL_CODE. "
            "List of prefixes can be found here: /show-countries"
        )
        self.make_invalid_requests(invalid_to_zipcode, expected_msg)

        # validate_postal_code validator not valid
        invalid_to_zipcode = deepcopy(self.valid_data)
        invalid_to_zipcode["delivery_address"]["to_zipcode"] = "BGR:DAS"
        expected_msg = "Postal Code is not valid!"
        self.make_invalid_requests(invalid_to_zipcode, expected_msg)

    def test_order_delivery_type_invalid_enum_value(self):
        """
        Test passing invalid delivery type
        """

        # invalid enum
        not_valid_data = deepcopy(self.valid_data)
        not_valid_data["delivery_type"] = "notvalidData"
        expected_msg = (
            "Invalid payload {'delivery_type': ['Invalid enum member notvalidData']}"
        )
        self.make_invalid_requests(not_valid_data, expected_msg)

        # missing delivery_type
        missing_delivery_type = deepcopy(self.valid_data)
        del missing_delivery_type["delivery_type"]
        expected_msg = (
            "Invalid payload {'delivery_type': ['Missing data for required field.']}"
        )
        self.make_invalid_requests(missing_delivery_type, expected_msg)

    def test_delivery_type_valid_price_increment(self):
        """
        Check if the final price is correctly incremented based on the delivery type
        """
        country_regular_delivery_price = self.county.regular_delivery_price
        country_fast_delivery_price = self.county.fast_delivery_price
        country_express_delivery_price = self.county.express_delivery_price

        # create item with required stocks:
        quantity_to_order = self.valid_data["items"][0]["quantity"]
        item: ItemModel = ItemFactory(id=1, stocks=quantity_to_order)
        item_regular_price: float = item.price
        expected_item_total_order_price = item_regular_price * quantity_to_order

        # check db initial status
        orders: list[OrderModel] = OrderModel.query.all()
        self.assertEqual(len(orders), 0)

        # place express order
        self.make_valid_request(
            data_to_use=self.valid_data,
            expected_total_order_cost=expected_item_total_order_price,
            expected_payed_delivery=country_express_delivery_price,
            expected_orders_in_db=1,
        )

        # place fast order
        self.valid_data["delivery_type"] = "fast"
        self.make_valid_request(
            data_to_use=self.valid_data,
            expected_total_order_cost=expected_item_total_order_price,
            expected_payed_delivery=country_fast_delivery_price,
            expected_orders_in_db=2,
        )

        # place regular order
        self.valid_data["delivery_type"] = "regular"
        self.make_valid_request(
            data_to_use=self.valid_data,
            expected_total_order_cost=expected_item_total_order_price,
            expected_payed_delivery=country_regular_delivery_price,
            expected_orders_in_db=3,
        )

    def test_valid_order_with_multiple_items(self):
        """
        Test the option to add multiple items in an order
        """
        self.valid_data["items"].append({"prod_id": 2, "quantity": 2})

        all_items: list[ItemModel] = ItemModel.query.all()
        self.assertEqual(len(all_items), 0)

        for indx in range(2):
            ItemFactory(id=indx + 1, stocks=2)

        all_items: list[ItemModel] = ItemModel.query.all()
        self.assertEqual(len(all_items), 2)

        expected_total_order_cost: float = 0

        for item in self.valid_data["items"]:
            prod_id: int = item.get("prod_id")
            specific_item: ItemModel = ItemModel.query.filter_by(id=prod_id).scalar()
            expected_total_order_cost += item.get("quantity") * specific_item.price

        self.make_valid_request(
            data_to_use=self.valid_data,
            expected_total_order_cost=expected_total_order_cost,
            expected_payed_delivery=self.county.express_delivery_price,
            expected_orders_in_db=1,
        )

    def test_get_all_order_per_user(self):
        """
        Test if user can access all of his orders
        """
        for indx in range(1, 2):
            # create users. Users with id 0 1 already exist from headers and Country
            UserFactory(id=indx + 1)

        for indx in range(5):
            # create users orders
            if indx % 2 != 0:
                OrderFactory(id=indx + 1, customer_id=2)
            else:
                OrderFactory(id=indx + 1, customer_id=0)

        # test number of orders
        user_with_id_zero_orders = OrderModel.query.filter_by(customer_id=0).all()
        self.assertEqual(len(user_with_id_zero_orders), 3)
        user_with_id_two_orders = OrderModel.query.filter_by(customer_id=2).all()
        self.assertEqual(len(user_with_id_two_orders), 2)

        # test correct order ids
        user_with_id_zero_orders_ids = [o.id for o in user_with_id_zero_orders]
        self.assertEqual(user_with_id_zero_orders_ids, [1, 3, 5])
        user_with_id_two_orders_ids = [o.id for o in user_with_id_two_orders]
        self.assertEqual(user_with_id_two_orders_ids, [2, 4])

    def test_change_order_status_to_dispatched(self):
        """
        Test the behavior of order status changes
        """
        # TODO MOCK DISCORD AND/OR MOVE TO OTHER TEST SUIT?

        # initial state
        order: OrderModel = OrderFactory(id=1)
        self.assertEqual(order.status, OrderStatus.new)

        # permission error
        resp = self.client.post(
            "/dispatcher/dispatch", headers=self.headers, json={"order_id": 1}
        )
        permission_required = resp.json["message"]
        self.assertEqual(
            permission_required, "You do not have permissions to access this resource"
        )

        # successfully change
        self.headers = self.return_user_headers(UserRole.dispatcher)
        resp = self.client.post(
            "/dispatcher/dispatch", headers=self.headers, json={"order_id": 1}
        )
        self.assert200(resp)
        self.assertEqual(order.status, OrderStatus.dispatched)

    def test_change_order_payment_status(self):
        """
        Test the behavior of order status changes
        """
        # TODO MOCK PAYPAL AND/OR MOVE TO OTHER TEST SUIT?
