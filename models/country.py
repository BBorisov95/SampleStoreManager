from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from db import db


class CountryModel(db.Model):
    __tablename__ = "country"
    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    country_name: Mapped[str] = mapped_column(
        db.String(255), nullable=False, unique=True
    )
    prefix: Mapped[str] = mapped_column(db.String(255), nullable=False)
    regular_delivery_price: Mapped[float] = mapped_column(db.Float(), nullable=False)
    fast_delivery_price: Mapped[float] = mapped_column(db.Float(), nullable=False)
    express_delivery_price: Mapped[float] = mapped_column(db.Float(), nullable=False)
    currency: Mapped[str] = mapped_column(db.String(5), nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, server_default=func.now())
    last_update_by: Mapped[int] = mapped_column(
        db.Integer(), db.ForeignKey("users.id")
    )
