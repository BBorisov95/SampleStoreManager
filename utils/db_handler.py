from sqlalchemy.exc import IntegrityError, PendingRollbackError
from werkzeug.exceptions import Conflict

from db import db

msg_mapper = {
    "UserModel": "User with this username or email already exist!",
    "ItemModel": "Item with this part number already exist!",
}


def do_commit(obj: db.Model):
    try:
        db.session.add(obj)
        db.session.flush()
    except (IntegrityError, PendingRollbackError):
        """
        Constrains violations like user with such email exist or item with such part_number
        """
        msg = msg_mapper.get(obj.__class__.__name__)

        raise Conflict(description=msg)
