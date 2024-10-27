from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models.user import UserModel


class PayPalTransactionModel(db.Model):

    __tablename__ = "paypal"
    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    paypal_transaction_id: Mapped[str] = mapped_column(db.String(), nullable=False)
    status: Mapped[str] = mapped_column(db.String(), nullable=False)
    internal_user_id: Mapped[int] = mapped_column(
        db.Integer(), db.ForeignKey("users.id"), nullable=False
    )
    paypal_customer_acc_id: Mapped[str] = mapped_column(
        db.String(), nullable=True
    )  # payer_id paypal id
    transaction_amount: Mapped[float] = mapped_column(
        db.Float(), nullable=False
    )  # payment amount
    transaction_currency: Mapped[str] = mapped_column(db.String(), nullable=False)
    reference_id: Mapped[int] = mapped_column(
        db.Integer(), nullable=False
    )  # our order_id
    created_at: Mapped[datetime] = mapped_column(db.DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, server_default=func.now())

    user: Mapped["UserModel"] = relationship("UserModel", backref="paypal")
