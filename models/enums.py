from enum import Enum


class UserRole(Enum):
    admin = "Server Admin"
    regular = "User"
    manager = "Store Manager"
    dispatcher = "Dispatcher"
    data_entry = "Data Entry Staff member"


class OrderStatus(Enum):
    new = "Waiting to process the order."
    dispatched = "The order is collected by dispatcher."
    shipped = "The order is shipped."
    received = "The order is received by customer."


class DeliveryType(Enum):
    regular = "From 4 to 5 days"
    fast = "From 2 to 3 days"
    express = "Next day delivery"


class PaymentStatus(Enum):
    unpaid = "The order is not paid!"
    paid = "The order is successfully paid!"
    refunded = "The order is refunded!"
