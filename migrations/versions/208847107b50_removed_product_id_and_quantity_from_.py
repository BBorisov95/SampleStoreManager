"""removed product_id and quantity from orderModel -> moved them to new ClientBasket (new model) Manual added alter and create enum types.

Revision ID: 208847107b50
Revises: f643b50fe5f6
Create Date: 2024-10-18 22:31:26.515061

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "208847107b50"
down_revision = "f643b50fe5f6"
branch_labels = None
depends_on = None


def upgrade():
    # ### custom commands
    """
    added new user role
    + created new enums
    """
    op.execute("ALTER TYPE userrole ADD VALUE 'data_entry' AFTER 'dispatcher';")
    op.execute("CREATE TYPE deliverytype AS ENUM ('regular', 'fast', 'express');")
    op.execute("CREATE TYPE paymentstatus AS ENUM ('unpaid', 'paid', 'refunded');")
    """
    DO NOT FORGET TO DISCONNECT AND RECONNECT THE DB, OTHERWISE WILL NOT BE SHOWN!
    """
    # ### end of custom commands

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "client_basket",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("orders", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "delivery_type",
                sa.Enum("regular", "fast", "express", name="deliverytype"),
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "payment_status",
                sa.Enum("unpaid", "paid", "refunded", name="paymentstatus"),
                nullable=False,
            )
        )
        batch_op.add_column(sa.Column("total_order", sa.Float(), nullable=False))
        batch_op.drop_column("product_id")
        batch_op.drop_column("quantity")

    # ### end Alembic commands ###


def downgrade():
    # ### custom commands
    op.execute("UPDATE users SET role = 'regular' WHERE role = 'data_entry';")
    op.execute(
        "CREATE TYPE userrole_new AS ENUM ('admin','regular', 'manager', 'dispatcher');"
    )  # create new table
    op.execute(
        "ALTER TABLE users ALTER COLUMN role TYPE userrole_new USING role::text::userrole_new;"
    )  # alter the tables using userrole to the new userrole
    op.execute("DROP TYPE userrole;")  # delete old userrole
    op.execute(
        "ALTER TYPE userrole_new RENAME TO userrole;"
    )  # rename the new userole as the old one

    # ### end of custom commands

    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("orders", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "quantity",
                sa.INTEGER(),
                autoincrement=False,
                nullable=False,
                server_default="0",
            )
        )
        batch_op.add_column(
            sa.Column("product_id", sa.INTEGER(), autoincrement=False, nullable=True)
        )
        batch_op.drop_column("total_order")
        batch_op.drop_column("payment_status")
        batch_op.drop_column("delivery_type")

    op.drop_table("client_basket")
    # ### end Alembic commands ###
    """
    DELETE THE ENUMS TYPES
    """
    op.execute("DROP TYPE paymentstatus;")
    op.execute("DROP TYPE deliverytype;")
