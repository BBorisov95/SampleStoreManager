from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from db import db


class Logs(db.Model):
    """
    Will make records of all activities for orders
    such as:
    user_id: did this for order
    """

    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    user_id: Mapped[int] = mapped_column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    prod_id: Mapped[int] = mapped_column(db.Integer(), db.ForeignKey("items.id"))
    order_id: Mapped[int] = mapped_column(db.Integer(), db.ForeignKey("orders.id"))
    log_info: Mapped[str] = mapped_column(db.Text(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, server_default=func.now())
