from urllib.parse import urljoin
from uuid import uuid4

import requests as r
from decouple import config
from requests.auth import HTTPBasicAuth
from werkzeug.exceptions import BadRequest

from models.client_basket import ClientBasket
from models.item import ItemModel
from models.order import OrderModel
from services.paypal.fragments.purchase_unit import PurchaseUnit
from services.paypal.utils.make_units import make_unit


class PayPal:

    BASE_URL = config("paypal_url")
    __PPRI = str(uuid4())

    def __init__(self):
        self.brand_name = config("pp_brand_name")
        self.headers = {
            "Content-Type": "application/json",
            "PayPal-Request-Id": self.__PPRI,  # used over all requests on the instance
        }
        self.__do_auth()

    def __do_auth(self) -> None:
        """
        Whenever executed attach a Bearer token to headers
        :return: None -> update instance attribute
        """
        link = "v1/oauth2/token"
        auth = HTTPBasicAuth(config("paypal_client_id"), config("paypal_client_secret"))
        aut_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials"}
        response = r.post(
            urljoin(self.BASE_URL, link), auth=auth, headers=aut_headers, data=data
        )

        self.headers["Authorization"] = (
            "Bearer" + " " + response.json().get("access_token")
        )

    def init_payment(
        self,
        order_instance: OrderModel,
        ordered_products_information: list[tuple[ItemModel, ClientBasket]],
    ):
        link = "v2/checkout/orders"
        make_unit(
            order_information=ordered_products_information,
            order_instance=order_instance,
        )
        purchase_units = [unit.to_dict() for unit in PurchaseUnit.units]
        data = {
            "intent": "CAPTURE",  # to receive the money
            "purchase_units": purchase_units,
            "payment_source": {
                "paypal": {
                    "experience_context": {
                        "brand_name": self.brand_name,
                        "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                        "locale": "en-US",
                        "landing_page": "LOGIN",
                        "shipping_preference": "NO_SHIPPING",
                        "user_action": "PAY_NOW",
                        "return_url": f"{config('dns')}/paypal-redirect/approve",
                        # FE to return to specific page when payed
                        "cancel_url": f"{config('dns')}/paypal-redirect/decline/{order_instance.id}",
                        # FE to return to specific page when failed to pay
                    }
                }
            },
        }
        response = r.post(
            urljoin(self.BASE_URL, link), headers=self.headers, json=data
        ).json()
        if not response.get("debug_id"):
            status = response.get("status")
            amount = data.get("purchase_units")[0].get("amount").get("value")
            currency = data.get("purchase_units")[0].get("amount").get("currency_code")
            order_id = response.get("id")
            payer_confirm = [
                link.get("href")
                for link in response.get("links")
                if link.get("rel") == "payer-action"
            ]
            return order_id, payer_confirm, status, amount, currency
        return BadRequest(
            f"We are really sorry for the inconvenience! Please contact our support!"
        )

    def confirm_order(self, order_id):
        link = f"/v2/checkout/orders/{order_id}/confirm-payment-source"
        data = {
            "processing_instruction": "ORDER_COMPLETE_ON_PAYMENT_APPROVAL",
            "payment_source": {
                "paypal": {
                    "experience_context": {
                        "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                        "brand_name": self.brand_name,
                        "locale": "en-US",
                        "landing_page": "LOGIN",
                        "shipping_preference": "SET_PROVIDED_ADDRESS",
                        "user_action": "PAY_NOW",
                    },
                }
            },
        }

        response = r.post(
            url=urljoin(self.BASE_URL, link), headers=self.headers, json=data
        )
        return response

    def capture_order(self, order_id):
        link = f"/v2/checkout/orders/{order_id}/capture"
        response = r.post(urljoin(self.BASE_URL, link), headers=self.headers).json()
        return response
