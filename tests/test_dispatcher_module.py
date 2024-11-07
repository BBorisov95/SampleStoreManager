from datetime import datetime
from unittest.mock import patch

from models import OrderModel, OrderStatus, UserRole
from services.discord.discord_bot import DiscordBot
from tests.base_functionalities import APIBaseTestCase


class TestDispatcherModule(APIBaseTestCase):
    """
    Test suite for dispatch related endpoints
    and behaviors on orders models.
    """

    def setUp(self):
        super().setUp()
        self.headers: dict = self.return_user_headers(for_role=UserRole.dispatcher)
        self.order: OrderModel = self.create_order_which_has_client_basket_records()

    def test_get_orders_for_dispatch(self):
        """
        Test a get requests and successful return DispatchOrderResponseSchema
        :return:
        """

        resp = self.client.get("/dispatcher/get-orders", headers=self.headers)
        self.assert200(resp)

        expected_msg = [
            {
                "id": self.order.id,
                "customer_id": self.order.customer_id,
                "status": self.order.status.value,
                "delivery_type": self.order.delivery_type.value,
                "delivery_address": {
                    "to_country": self.order.to_country,
                    "to_city": self.order.to_city,
                    "to_street_address": self.order.to_street_address,
                    "to_building_number": self.order.to_building_number,
                    "to_zipcode": self.order.to_zipcode,
                },
                "created_at": datetime.strftime(
                    self.order.created_at, "%Y-%m-%dT%H:%M:%S.%f"
                ),
            }
        ]

        self.assertEqual(expected_msg, resp.json["all_order_for_dispatch"])

    @patch.object(DiscordBot, "send_msg")
    def test_change_order_status_to_dispatched(self, mock_discord: patch):
        """
        Test the behavior of order status changes
        """

        # initial state
        self.assertEqual(self.order.status, OrderStatus.new)

        # successfully change
        resp = self.client.post(
            "/dispatcher/dispatch", headers=self.headers, json={"order_id": 1}
        )
        self.assert200(resp)
        self.assertEqual(self.order.status, OrderStatus.dispatched)
        mock_discord.assert_called_once_with(1, "dispatch")

    def test_mark_order_as_shipped(self):
        """
        Test if order will be marked as shipped when endpoint is triggerd
        :return:
        """

        resp = self.client.put(
            f"/dispatcher/approve-shipped/{self.order.id}", headers=self.headers
        )
        self.assertEqual(resp.status_code, 201)

        order: OrderModel = OrderModel.query.filter_by(id=self.order.id).scalar()
        self.assertEqual(order.status, OrderStatus.shipped.name)
