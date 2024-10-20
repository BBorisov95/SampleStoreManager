from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models.item import ItemModel
from models.order import OrderModel


class ClientBasket(db.Model):
    """
    This model will hold the information about
    the purchased products in an order.
    """

    __tablename__ = "client_basket"
    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        db.Integer(), db.ForeignKey("orders.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        db.Integer(), db.ForeignKey("items.id"), nullable=False
    )
    product_sold_price: Mapped[float] = mapped_column(db.Float(), nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer(), nullable=False, default=1)

    item: Mapped["ItemModel"] = relationship(
        "ItemModel", foreign_keys=[product_id]
    )  # fk must be list
    order: Mapped["OrderModel"] = relationship("OrderModel", backref="client_basket")
