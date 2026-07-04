"""create users table

Revision ID: 3e6292fdfb7e
Revises:
Create Date: 2026-07-01 17:53:41.497314

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e6292fdfb7e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("city", sa.String, default="Москва", nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
