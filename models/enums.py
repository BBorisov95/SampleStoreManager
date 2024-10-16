from enum import Enum


class UserRole(Enum):
    regular = "User"
    manager = "Store Manager"
    dispatcher = "Dispatcher"
    data_entry = "Data Entry Staff member"


class OrderStatus(Enum):
    new = "Waiting to process the order."
    dispatched = "The order is collected by dispatcher."
    shipped = "The order is shipped."
    received = "The order is received by customer."
