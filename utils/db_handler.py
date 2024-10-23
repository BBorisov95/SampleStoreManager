from sqlalchemy.exc import IntegrityError, PendingRollbackError
from werkzeug.exceptions import Conflict

from db import db
from sqlalchemy import event
from sqlalchemy.orm.attributes import get_history
from models.operational_logs import Logs
from models import ItemModel, UserModel, OrderModel, ClientBasket

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


@event.listens_for(ItemModel, "after_update")
@event.listens_for(OrderModel, "after_update")
def track_item_update(mapper, connection, target: db.Model):
    """
    Log all changes made for item
    :param mapper: sql.mapper -> point to Target
    :param connection: session connection
    :param target: ItemModel
    :return: None add new record to db
    """
    change_msg_to_commit: str = "User {user} "
    has_any_change, msg, user_id = check_for_changes(target)
    if has_any_change:
        log: Logs
        change_msg_to_commit = change_msg_to_commit.format(user=user_id)
        change_msg_to_commit += ';'.join(msg)
        if type(target) is OrderModel:
            log: Logs = Logs(user_id=user_id, order_id=target.id, log_info=change_msg_to_commit)
        if type(target) is ItemModel:
            log: Logs = Logs(user_id=user_id, prod_id=target.id, log_info=change_msg_to_commit)

        db.session.add(log)

@event.listens_for(ItemModel, "after_insert")
def track_item_create(mapper, connection, target: ItemModel):
    """
    Log all creation made for item
    :param mapper: sql.mapper -> point to Target
    :param connection: session connection
    :param target: ItemModel
    :return: None add new record to db
    """
    user_id = target.last_update_by
    msg = f"Created new item in db: {target.id} with id: {target.id}, name: {target.name}, price: {target.price}"
    log: Logs = Logs(user_id=user_id, prod_id=target.id, log_info=msg)
    db.session.add(log)


def check_for_changes(target: db.Model) -> tuple[bool, list[str], int or None]:
    """
    Check if the target element has changed in fields
    :param target: <any>db.Model
    :return: tuple(bool if changes found, str msg)
    """
    user_id: int or None = None
    change_msg_to_commit: list[str] = []
    has_any_change: bool = False
    for field in list(target.__dict__.keys())[1::]:
        state = get_history(target, field)
        if state.has_changes():
            if not has_any_change:
                user_id = target.last_update_by
                has_any_change = True
            if isinstance(target, ItemModel) and field == "specs":
                new_specs: dict = state.added[0]
                old_specs: dict = state.deleted[0]
                modified_values: dict = {
                    key: new_specs[key]
                    for key in new_specs
                    if new_specs[key] != old_specs.get(key)
                }
                for k, v in modified_values.items():
                    change_msg_to_commit.append(
                        f"Changed spec key: {k} to value: {v} from {old_specs.get('key')} "
                    )
                continue
            change_msg_to_commit.append(
                f"Changed {field} from {state.deleted} to {state.added}. "
            )
    return has_any_change, change_msg_to_commit, user_id
