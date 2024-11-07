from unittest.mock import patch

from models import (
    OrderModel,
    UserModel,
    ClientBasket,
    ItemModel,
    UserRole,
    PayPalTransactionModel,
    PaymentStatus,
)
from services.discord.discord_bot import DiscordBot
from services.paypal.paypal import PayPal
from tests.base_functionalities import APIBaseTestCase, generate_token
from tests.factories import PayPayTransactionFactory
from tests.factories import UserFactory


class TestPayPalModule(APIBaseTestCase):
    """
    Custom module which change the order payment status
    """

    def setUp(self):
        super().setUp()
        UserFactory(role=UserRole.admin)

    @patch.object(
        PayPal,
        "init_payment",
        return_value=[1, "some_link", "paypal_order_status", 12, "EUR"],
    )
    @patch.object(PayPal, "_PayPal__do_auth")
    def test_paying_foreign_order_raises_401(self, mock_paypal_auth, mock_paypal_payment):
        """
        Test the case where userA want to pay order for UserB
        """
        order: OrderModel = self.create_order_which_has_client_basket_records()
        original_customer_order_id: int = order.customer_id
        order.customer_id = 123  # JIC set big random number
        user_one: UserModel = UserFactory()
        token: dict = generate_token(user_one)
        headers: dict = {"Authorization": f"Bearer {token}"}

        resp = self.client.post(f"/user/order/{order.id}/pay", headers=headers)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(
            resp.json["message"], "Sorry you cannot pay for this order. It's not yours!"
        )

        valid_user: UserModel = UserModel.query.filter_by(
            id=original_customer_order_id
        ).scalar()  # user created by create_order_which_has_client_basket_records
        order.customer_id = original_customer_order_id  # return value for valid reqeust
        token: dict = generate_token(valid_user)
        headers: dict = {"Authorization": f"Bearer {token}"}
        valid_resp = self.client.post(f"/user/order/{order.id}/pay", headers=headers)
        self.assert200(valid_resp)
        self.assertEqual(valid_resp.json["order_confirm_link"], "some_link")
        mock_paypal_payment.assert_called_once()
        client_basket: ClientBasket = ClientBasket.query.filter_by(
            order_id=order.id
        ).scalar()
        item_in_basket: ItemModel = ItemModel.query.filter_by(
            id=client_basket.product_id
        ).scalar()
        mock_paypal_payment.assert_called_once_with(
            order, [(item_in_basket, client_basket)]
        )
        mock_paypal_auth.assert_called_once()

    @patch.object(DiscordBot, "send_msg")
    @patch.object(
        PayPal,
        "capture_order",
        return_value={
            "status": "COMPLETED",
        },
    )
    @patch.object(PayPal, "confirm_order")
    @patch.object(PayPal, "_PayPal__do_auth")
    def test_paypal_confirm_endpoint(
        self, mock_paypal_auth, mock_paypal_confirm_order, mock_paypal_capture_order, mock_discord_bot
    ):
        """
        Test the order change payment statuses
        """
        transaction: PayPalTransactionModel = PayPayTransactionFactory()
        order_id: int = transaction.reference_id

        order: OrderModel = OrderModel.query.filter_by(id=order_id).scalar()
        self.assertEqual(order.payment_status.value, PaymentStatus.unpaid.value)

        fake_token: str = transaction.paypal_transaction_id
        fake_payer_id: str = transaction.paypal_customer_acc_id
        mock_paypal_capture_order.return_value = {
            "status": "COMPLETED",
            "id": fake_token,
            "purchase_units": [{"reference_id": order_id}],
            "payer": {"payer_id": fake_payer_id},
        }
        resp = self.client.get(
            f"/paypal-redirect/approve?token={fake_token}&PayerID={fake_payer_id}"
        )
        self.assert200(resp)
        self.assertEqual(resp.json["message"], "Payment is successfully processed!")
        mock_paypal_confirm_order.assert_called_once_with(fake_token)
        mock_paypal_capture_order.assert_called_once_with(fake_token)
        self.assertEqual(mock_paypal_auth.call_count, 2)
        mock_discord_bot.assert_called_once_with(order_id, "payment_success")

        order: OrderModel = OrderModel.query.filter_by(id=order_id).scalar()
        self.assertEqual(order.payment_status, PaymentStatus.paid.name)

    def test_paypal_fail_confirm_endpoint(self):
        """
        Test cases where invalid approval link is tried to access
        """
        transaction: PayPalTransactionModel = PayPayTransactionFactory()

        order_id: int = transaction.reference_id
        fake_token: str = "transaction.paypal_transaction_id"
        fake_payer_id: str = transaction.paypal_customer_acc_id

        order: OrderModel = OrderModel.query.filter_by(id=order_id).scalar()
        self.assertEqual(order.payment_status.value, PaymentStatus.unpaid.value)

        resp = self.client.get(f"/paypal-redirect/approve?PayerID={fake_payer_id}")
        self.assert400(resp)
        self.assertEqual(resp.json["message"], "Missing token or payer ID.")

        resp = self.client.get(f"/paypal-redirect/approve?token={fake_token}")
        self.assert400(resp)
        self.assertEqual(resp.json["message"], "Missing token or payer ID.")

        order: OrderModel = OrderModel.query.filter_by(id=order_id).scalar()
        self.assertEqual(order.payment_status.value, PaymentStatus.unpaid.value)

    @patch.object(DiscordBot, "send_msg")
    def test_paypal_decline_endpoint(self, mock_discord):
        """
        Test when payment is decline
        :return:
        """
        transaction: PayPalTransactionModel = PayPayTransactionFactory()
        order_id: int = transaction.reference_id

        order: OrderModel = OrderModel.query.filter_by(id=order_id).scalar()
        self.assertEqual(order.payment_status.value, PaymentStatus.unpaid.value)

        resp = self.client.get(f"/paypal-redirect/decline/{order_id}")
        self.assert200(resp)
        self.assertEqual(resp.json["message"], "Payment Declined!")
        mock_discord.assert_called_once_with(order_id, "payment_failed")

        order: OrderModel = OrderModel.query.filter_by(id=order_id).scalar()
        self.assertEqual(order.payment_status.value, PaymentStatus.unpaid.value)
