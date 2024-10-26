from datetime import datetime
from sqlalchemy import JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from db import db


class ItemModel(db.Model):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float(), nullable=False)
    part_number: Mapped[str] = mapped_column(db.String(32), nullable=False, unique=True)
    ean: Mapped[int] = mapped_column(db.String(13))
    brand: Mapped[str] = mapped_column(
        db.String(32),
        nullable=False,
        default="dummy brand",
        server_default="dummy brand",
    )
    category: Mapped[str] = mapped_column(db.String(32), nullable=False)
    specs: Mapped[dict] = mapped_column(JSON, nullable=True)
    stocks: Mapped[int] = mapped_column(db.Integer(), nullable=False, default=0)
    sold_pieces: Mapped[int] = mapped_column(db.Integer(), nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, server_default=func.now())
    last_update_by: Mapped[int] = mapped_column(
        db.Integer(), db.ForeignKey("users.id")
    )
