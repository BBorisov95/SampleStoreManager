from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models.enums import OrderStatus


class OrderModel(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    customer_id: Mapped[int] = mapped_column(db.Integer(), nullable=False)
    product_id: Mapped[int] = mapped_column(db.Integer(), nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer(), nullable=False, default=1)
    ship_to: Mapped[str] = mapped_column(db.String(255), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        db.Enum(OrderStatus), nullable=False, default=OrderStatus.new.name
    )

    item: Mapped["ItemModel"] = relationship("ItemModel", back_populates="orders")
