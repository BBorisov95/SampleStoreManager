from werkzeug.exceptions import BadRequest

from db import db
from models.paypal_transactions import PayPalTransactionModel
from utils.db_handler import do_commit


class PayPalManger:

    @staticmethod
    def create_transaction(
        transaction_id: str,
        status: str,
        user_id: int,
        amount: float,
        currency: str,
        order_id: int,
    ):
        transaction: PayPalTransactionModel = PayPalTransactionModel(
            paypal_transaction_id=transaction_id,
            status=status,
            internal_user_id=user_id,
            transaction_amount=amount,
            transaction_currency=currency,
            reference_id=order_id,
        )
        do_commit(transaction)

    @staticmethod
    def update_transaction(transaction_id: str, **kwargs):
        requested_transaction: PayPalTransactionModel = db.session.execute(
            db.select(PayPalTransactionModel).filter_by(
                paypal_transaction_id=transaction_id
            )
        ).scalar()
        if not requested_transaction:
            raise BadRequest(f"Transaction not found!")
        for key, value in kwargs.items():
            setattr(requested_transaction, key, value)

        do_commit(requested_transaction)
