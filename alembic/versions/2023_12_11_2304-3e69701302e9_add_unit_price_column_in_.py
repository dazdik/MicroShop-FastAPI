"""add unit_price column in OrderProductAssociation

Revision ID: 3e69701302e9
Revises: 193e2b4ddb84
Create Date: 2023-12-11 23:04:48.267349

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3e69701302e9"
down_revision: Union[str, None] = "193e2b4ddb84"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "order_product_association",
        sa.Column("unit_price", sa.Integer(), server_default="0", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("order_product_association", "unit_price")
    # ### end Alembic commands ###
