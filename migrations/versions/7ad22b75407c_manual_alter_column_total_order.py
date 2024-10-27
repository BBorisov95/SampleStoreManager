"""manual alter column total_order for some reason alembic does not found default=0, server_default

Revision ID: 7ad22b75407c
Revises: df571be6c40c
Create Date: 2024-10-18 23:43:53.154401

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7ad22b75407c"
down_revision = "df571be6c40c"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("orders", schema=None) as batch_op:
        batch_op.alter_column(
            "total_order", server_default="0", existing_type=sa.Float(), nullable=False
        )


def downgrade():
    with op.batch_alter_table("orders", schema=None) as batch_op:
        batch_op.alter_column(
            "total_order", server_default=None, existing_type=sa.Float(), nullable=False
        )
