"""added brand filed to items

Revision ID: f643b50fe5f6
Revises: e02db421da03
Create Date: 2024-10-17 23:36:02.687809

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f643b50fe5f6"
down_revision = "e02db421da03"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "brand",
                sa.String(length=32),
                server_default="dummy brand",
                nullable=False,
            )
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.drop_column("brand")

    # ### end Alembic commands ###
