"""added CountryModel which hold info about countries and cost per delivery type, added new columns to orders for full adress info.'



Revision ID: ae2d78671e49
Revises: c8e20d4de9f8
Create Date: 2024-10-20 20:37:28.266154

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ae2d78671e49"
down_revision = "c8e20d4de9f8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "country",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("country_name", sa.String(length=255), nullable=False),
        sa.Column("prefix", sa.String(length=255), nullable=False),
        sa.Column("regular_delivery_price", sa.Float(), nullable=False),
        sa.Column("fast_delivery_price", sa.Float(), nullable=False),
        sa.Column("express_delivery_price", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=5), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("country_name"),
    )
    with op.batch_alter_table("orders", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("to_street_address", sa.String(length=255), nullable=False)
        )
        batch_op.add_column(
            sa.Column("to_building_number", sa.Integer(), nullable=False)
        )
        batch_op.add_column(
            sa.Column("payment_for_shipping", sa.Float(), nullable=False)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("orders", schema=None) as batch_op:
        batch_op.drop_column("payment_for_shipping")
        batch_op.drop_column("to_building_number")
        batch_op.drop_column("to_street_address")

    op.drop_table("country")
    # ### end Alembic commands ###
