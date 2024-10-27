from models.client_basket import ClientBasket
from models.country import CountryModel
from models.item import ItemModel
from models.order import OrderModel
from services.paypal.fragments.purchase_unit import PurchaseUnit


class PurchaseUnitsBuilder:

    def __init__(self):
        self.currency_code: CountryModel.currency = None
        self.value: ClientBasket.price = 0
        self.reference_id: ClientBasket.id = None
        self.items: list[dict] = []

    def set_currency_code(self, value: CountryModel):
        self.currency_code = value
        return self

    def set_value(self, value: ClientBasket):
        self.value += value.quantity * value.product_sold_price
        return self

    def set_reference_id(self, value: OrderModel):
        self.reference_id = value.id
        return self

    def set_items(
        self, item: ItemModel, client_basket: ClientBasket, order_instance: OrderModel
    ):
        item_name = item.name
        item_quantity = client_basket.quantity
        amount = client_basket.product_sold_price
        self.items.append(
            {
                "name": item_name,
                "quantity": item_quantity,
                "unit_amount": {
                    "currency_code": order_instance.order_currency,
                    "value": amount,
                },
            }
        )
        return self

    def build(self) -> PurchaseUnit:
        """
        Build the product
        :return: Products Object
        """
        return PurchaseUnit(self)
