from flask import request
from flask_restful import Resource
from werkzeug.exceptions import Unauthorized, BadRequest

from managers.authenticator import auth
from managers.order import OrderManager
from managers.paypal import PayPalManger
from models.client_basket import ClientBasket
from models.enums import OrderStatus, PaymentStatus
from models.item import ItemModel
from services.discord.discord_bot import DiscordBot
from services.paypal.paypal import PayPal


class PayOrder(Resource):

    @auth.login_required()
    def post(self, order_id):
        current_user = auth.current_user().id
        order = OrderManager.get_specific_order(order_id=order_id)
        if order.customer_id != current_user:
            raise Unauthorized(f"Sorry you cannot pay for this order. It's not yours!")
        ordered_products_information: list[tuple[ItemModel, ClientBasket]] = [
            op for op in OrderManager.get_items_of_order(order_id=order_id)
        ]

        payment_id, order_confirm_link, transaction_status, amount, currency = (
            PayPal().init_payment(order, ordered_products_information)
        )
        PayPalManger.create_transaction(
            transaction_id=payment_id,
            status=transaction_status,
            user_id=current_user,
            amount=amount,
            currency=currency,
            order_id=order_id,
        )
        return {"order_confirm_link": order_confirm_link}, 200


class PayPalConfirmRedirect(Resource):

    def get(self):
        token = request.args.get("token")
        payer_id = request.args.get("PayerID")

        if token and payer_id:
            PayPal().confirm_order(token)
            capture = PayPal().capture_order(token)
            status = capture.get("status")
            if status == "COMPLETED":
                order_id: int = capture.get("purchase_units")[0].get("reference_id")
                OrderManager.change_order_status(order_id, OrderStatus.received)
                OrderManager.change_order_payment_status(order_id, PaymentStatus.paid)
                DiscordBot().send_msg(order_id, "payment_success")
                payer_info = capture.get("payer").get("payer_id")
                PayPalManger.update_transaction(
                    transaction_id=capture.get("id"),
                    status=status,
                    paypal_customer_acc_id=payer_info,
                )
                return {"message": "Payment is successfully processed!"}
        else:
            return BadRequest("Missing token or payer ID.")


class PayPalDeclineRedirect(Resource):
    def get(self, order_id):
        DiscordBot().send_msg(order_id, "payment_failed")
        return BadRequest(f"Payment Declined!")
