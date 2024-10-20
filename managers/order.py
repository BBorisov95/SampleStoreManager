from werkzeug.exceptions import NotFound

from db import db
from managers.item import ItemManager
from managers.country import CountryManager
from models.client_basket import ClientBasket
from models.enums import OrderStatus, DeliveryType
from models.order import OrderModel
from models.user import UserModel
from utils.db_handler import do_commit


class OrderManager:
    """
    Handle the logic for
    orders statuses
    """

    @staticmethod
    def place_order(user_obj: UserModel, order_data: dict):
        """
        Create Order and distribute between client basket and order tables
        :param user_obj: user model
        :param order_data: dict with info
        :return: OrderModel
        """
        baskets = []
        total_price = 0

        for item in order_data.get("items"):
            item_id = item.get("prod_id")
            item_quantity = item.get("quantity")
            item_obj = ItemManager.get_item(item_id)
            item_price: float = item_obj.price
            ItemManager.increase_sold_pcs(item_obj, item_quantity)

            basket = ClientBasket(
                product_id=item_id,
                quantity=item_quantity,
                product_sold_price=item_price
            )
            total_price += item_price
            baskets.append(basket)

        to_insert_order_data: dict = {"customer_id": user_obj.id}
        delivery_info = order_data.get("delivery_address")
        deliver_to_country = delivery_info.get("to_country")
        delivery_type = order_data.get("delivery_type")
        delivery_tax = CountryManager.get_delivery_tax(
            deliver_to_country, delivery_type
        )
        to_insert_order_data.update({"payment_for_shipping": delivery_tax})

        to_insert_order_data.update(**delivery_info)
        new_order: OrderModel = OrderModel(**to_insert_order_data)
        new_order.total_order = total_price
        if hasattr(DeliveryType, delivery_type):
            new_order.delivery_type = getattr(DeliveryType, delivery_type)
        do_commit(new_order)
        for basket in baskets:
            basket.order_id = new_order.id
            db.session.add(basket)
        user_obj.number_of_orders += 1
        do_commit(user_obj)
        return new_order

    @staticmethod
    def change_order_status(order_id: int, change_status_to: OrderStatus):

        requested_order: OrderModel = db.session(
            db.select(OrderModel).filder_by(id=order_id)
        ).scalar()
        if not requested_order:
            raise NotFound(f"Order with id {order_id} not found!")

        requested_order.status = change_status_to
        do_commit(requested_order)

    @staticmethod
    def get_all_my_orders(user_id: int):
        all_orders = db.session.execute(db.select(OrderModel).filter_by(customer_id=user_id)).scalars()
        if not all_orders:
            raise NotFound(f'No orders found!')
        return all_orders
