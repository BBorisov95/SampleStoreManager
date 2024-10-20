from sqlalchemy.orm import Mapped, mapped_column

from db import db
from models.enums import OrderStatus, DeliveryType, PaymentStatus


class OrderModel(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    customer_id: Mapped[int] = mapped_column(db.Integer(), nullable=False)
    to_country: Mapped[str] = mapped_column(db.String(255), nullable=False)
    to_city: Mapped[str] = mapped_column(db.String(255), nullable=False)
    to_zipcode: Mapped[str] = mapped_column(db.String(255), nullable=False)
    to_street_address: Mapped[str] = mapped_column(db.String(255), nullable=False)
    to_building_number: Mapped[int] = mapped_column(db.Integer(), nullable=False)
    payment_for_shipping: Mapped[float] = mapped_column(db.Float(), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        db.Enum(OrderStatus), nullable=False, default=OrderStatus.new
    )
    delivery_type: Mapped[DeliveryType] = mapped_column(
        db.Enum(DeliveryType),
        nullable=False,
        default=DeliveryType.regular,
    )
    payment_status: Mapped[PaymentStatus] = mapped_column(
        db.Enum(PaymentStatus),
        nullable=False,
        default=PaymentStatus.unpaid,
    )
    total_order: Mapped[float] = mapped_column(db.Float(), nullable=False, default=0)
