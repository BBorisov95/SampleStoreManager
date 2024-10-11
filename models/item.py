from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models.order import OrderModel


class ItemModel(db.Model):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[str] = mapped_column(db.Float(), nullable=False)
    part_number: Mapped[str] = mapped_column(db.String(32), nullable=False, unique=True)
    ean: Mapped[int] = mapped_column(db.Integer())
    category: Mapped[str] = mapped_column(db.String(32), nullable=False)
    specs: Mapped[dict] = mapped_column(JSON, nullable=True)
    stocks: Mapped[int] = mapped_column(db.Integer(), nullable=False, default=0)
    sold_pieces: Mapped[int] = mapped_column(db.Integer(), nullable=False, default=0)

    orders: Mapped[list[OrderModel]] = relationship(
        "OrderModel", back_populates="items"
    )
