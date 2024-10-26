from sqlalchemy import desc, asc, func
from werkzeug.exceptions import NotFound, BadRequest

from db import db
from managers.order import OrderManager
from models.order import OrderModel
from models.enums import OrderStatus
from models.client_basket import ClientBasket
from models.item import ItemModel

from services.discord.discord_bot import DiscordBot


class DispatcherManager:

    @staticmethod
    def get_all_orders_for_dispatch():
        """
        Execute query to get all new orders sorted by delivery_type and date of creation
        :return: iterable
        """
        all_orders = (
            db.session.execute(
                db.select(
                    OrderModel.id,
                    OrderModel.customer_id,
                    OrderModel.status,
                    OrderModel.delivery_type,
                    OrderModel.created_at,
                    func.json_build_object(
                        "to_country",
                        OrderModel.to_country,
                        "to_city",
                        OrderModel.to_city,
                        "to_street_address",
                        OrderModel.to_street_address,
                        "to_building_number",
                        OrderModel.to_building_number,
                        "to_zipcode",
                        OrderModel.to_zipcode,
                    ).label("delivery_address"),
                )
                .distinct(OrderModel.id)
                .join(ClientBasket, ClientBasket.order_id == OrderModel.id)
                .join(ItemModel, ItemModel.id == ClientBasket.product_id)
                .filter(OrderModel.status == "new", ItemModel.stocks > 0)
                .order_by(
                    OrderModel.id,
                    desc(OrderModel.delivery_type),
                    asc(OrderModel.created_at),
                )
            )
        ).all()
        if not all_orders:
            NotFound("No orders found for dispatch!")
        return all_orders

    @staticmethod
    def dispatch_item(order_data: dict):
        order_id = order_data.get("order_id")
        last_updated_by = order_data.get('last_update_by')
        order = OrderManager.get_specific_order(order_id)
        if not order:
            raise NotFound(f"Order with id: {order_id} not found!")
        if order.status == OrderStatus.dispatched:
            raise BadRequest(f"Order {order_id} already dispatched!")
        order_elements: list[tuple] = OrderManager.get_items_of_order(order_id)

        try:
            for item, sold_pcs in order_elements:
                DispatcherManager.reduce_item_quantity(item, sold_pcs, last_updated_by)

            order.status = OrderStatus.dispatched
            order.last_update_by = last_updated_by
            db.session.add(order)
            db.session.flush()
            DiscordBot().send_msg(order_id)
        except BadRequest as be:
            db.session.rollback()
            raise be

    @staticmethod
    def approve_order_as_shipped(order_id: int, user_id: int):
        """
        Assume that all items are collected and can be marked as shipped
        :return:
        """
        OrderManager.change_order_status(
            order_id=order_id, change_status_to=OrderStatus.shipped,
            modify_by=user_id
        )

    @staticmethod
    def reduce_item_quantity(prod: ItemModel, required_quantity: int, last_updated_by: int):
        """
        If item is collected by dispatcher
        reduce stocks in warehouse
        :return: Rises or None
        """
        if prod.stocks == 0:
            raise BadRequest(
                f"Sorry It looks like that the {prod.name} is out of stock! Would you like to replace it?"
            )

        if prod.stocks < required_quantity:
            raise BadRequest(
                f"Oh no...It looks like that the {prod.name} does not have enough quantity to fulfill your order!"
                f" We have {prod.stocks} out of {required_quantity} pcs."
            )
        prod.stocks -= required_quantity
        prod.last_update_by = last_updated_by
