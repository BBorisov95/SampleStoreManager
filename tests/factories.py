from datetime import datetime

import factory
from werkzeug.security import generate_password_hash

from db import db
from models import (
    UserModel,
    UserRole,
    ItemModel,
    OrderModel,
    CountryModel,
    PayPalTransactionModel,
)
from models.enums import OrderStatus, PaymentStatus, DeliveryType

"""
to get all faker providers
from faker import Faker
fake = Faker()
print(fake.providers)
https://faker.readthedocs.io/en/master/providers.html
"""


class BaseFactory(factory.Factory):
    """
    Base Factory which handles the creation of an object
    """

    @classmethod
    def create(cls, **kwargs):
        create_object: factory.Factory = super().create(**kwargs)
        if hasattr(create_object, "password:"):
            """
            Only for user to insert the password as hash
            so we can test the proper login as well.
            """
            plain_pass: str = create_object.password
            create_object.password = generate_password_hash(
                plain_pass, method="pbkdf2:sha256"
            )
        db.session.add(create_object)
        db.session.flush()
        return create_object


class UserFactory(BaseFactory):
    """
    User creation factory
    Always generate random values
    """

    class Meta:
        model: UserModel = UserModel

    id: int = factory.Sequence(lambda n: n)
    email: str = factory.Faker("email")
    password: str = factory.Faker("password")
    username: str = factory.Faker("user_name")
    first_name: str = factory.Faker("first_name")
    last_name: str = factory.Faker("last_name")
    role: UserRole = UserRole.regular


class ItemFactory(BaseFactory):
    """
    Item creation factory
    Create a random item
    """

    class Meta:
        model: ItemModel = ItemModel

    id: int = factory.Sequence(lambda n: n)
    name: str = factory.Faker("name")
    price: float = factory.Faker(
        "pyfloat", left_digits=3, right_digits=2, positive=True
    )
    part_number: str = factory.Faker("isbn13")
    ean: int = factory.Faker("ean", length=13)
    brand: str = factory.Faker("company")
    category: str = factory.Faker("word")
    specs: dict = factory.Dict({})
    stocks: int = factory.Faker("random_int", min=1, max=10)
    sold_pieces: int = factory.Faker("random_int", min=0, max=10)
    created_at: datetime = factory.LazyFunction(datetime.utcnow)
    updated_at: datetime = factory.LazyFunction(datetime.utcnow)
    last_update_by: int = factory.LazyAttribute(lambda _: UserFactory().id)


class OrderFactory(BaseFactory):
    """
    Order creation factory
    use random data
    """

    class Meta:
        model = OrderModel

    id: int = factory.Sequence(lambda n: n + 1)
    customer_id: int = factory.Faker("random_int", min=1, max=1000)
    to_country: str = factory.Faker("country")
    to_city: str = factory.Faker("city")
    to_zipcode: str = factory.Faker("postcode")
    to_street_address: str = factory.Faker("street_address")
    to_building_number: int = factory.Faker("random_int", min=1, max=100)
    payment_for_shipping: float = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True
    )
    status: OrderStatus = factory.Iterator(OrderStatus)
    delivery_type: DeliveryType = DeliveryType.regular
    payment_status: PaymentStatus = PaymentStatus.unpaid
    total_order: float = factory.Faker(
        "pyfloat", left_digits=3, right_digits=2, positive=True
    )
    order_currency: str = "EUR"
    created_at: datetime = factory.LazyFunction(datetime.utcnow)
    updated_at: datetime = factory.LazyFunction(datetime.utcnow)
    last_update_by: int = factory.LazyAttribute(
        lambda _: UserFactory().id
    )  # Creates a User and assigns their ID


class CountryFactory(BaseFactory):
    """
    Create random Country
    """

    class Meta:
        model = CountryModel

    id: int = factory.Sequence(lambda n: n + 1)
    country_name: str = factory.Faker("country")
    prefix: str = factory.Faker("country_code")
    regular_delivery_price: float = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True
    )
    fast_delivery_price: float = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True
    )
    express_delivery_price: float = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True
    )
    currency: str = factory.Faker("currency_code")
    created_at: datetime = factory.LazyFunction(datetime.utcnow)
    updated_at: datetime = factory.LazyFunction(datetime.utcnow)
    last_update_by: int = factory.LazyAttribute(
        lambda _: UserFactory(role=UserRole.manager).id
    )


class PayPayTransactionFactory(BaseFactory):
    """
    Create random PayPal transction
    """

    class Meta:
        model = PayPalTransactionModel

    id: int = factory.Sequence(lambda n: n + 1)
    paypal_transaction_id: str = factory.Faker("swift8")
    status: str = factory.LazyAttribute(lambda _: "NEW")
    internal_user_id: int = factory.LazyAttribute(lambda _: UserFactory().id)
    paypal_customer_acc_id: str = factory.Faker("sbn9")
    transaction_amount: float = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True
    )
    transaction_currency: str = factory.LazyAttribute(lambda _: "EUR")
    reference_id: int = factory.LazyAttribute(lambda _: OrderFactory().id)
    created_at: datetime = factory.LazyFunction(datetime.utcnow)
    updated_at: datetime = factory.LazyFunction(datetime.utcnow)
