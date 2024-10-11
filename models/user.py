from sqlalchemy.orm import Mapped, mapped_column

from db import db
from models.enums import UserRole


class UserModel(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
    email: Mapped[str] = mapped_column(db.String(40), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    username: Mapped[str] = mapped_column(db.String(25), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        db.Enum(UserRole), default=UserRole.regular.name, nullable=False
    )
    number_of_orders: Mapped[int] = mapped_column(
        db.Integer(), nullable=False, default=0
    )
