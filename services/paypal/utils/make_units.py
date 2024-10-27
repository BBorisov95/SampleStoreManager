from models.client_basket import ClientBasket
from models.item import ItemModel
from models.order import OrderModel
from services.paypal.utils.purchase_units_builder import PurchaseUnitsBuilder


def make_unit(
    order_information: list[tuple[ItemModel, ClientBasket]], order_instance: OrderModel
):
    builder = PurchaseUnitsBuilder()
    builder.set_currency_code(order_instance.order_currency)
    builder.set_reference_id(order_instance)
    for item_unit, client_basket in order_information:
        builder.set_value(client_basket)
        builder.set_items(
            item=item_unit, client_basket=client_basket, order_instance=order_instance
        )
    builder.build()
