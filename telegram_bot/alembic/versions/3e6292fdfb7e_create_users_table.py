"""create users table

Revision ID: 3e6292fdfb7e
Revises:
Create Date: 2026-07-01 17:53:41.497314

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3e6292fdfb7e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("chat_id", sa.BigInteger, unique=True, nullable=True),
        sa.Column("city", sa.String, server_default="Москва", nullable=False),
        sa.Column("timezone", sa.SmallInteger, server_default=sa.text("3")),
        sa.Column("notification_status", sa.Boolean, server_default=sa.false()),
        sa.Column("local_time", sa.String, server_default="09:00"),
        sa.Column("utc_minutes", sa.Integer, server_default=sa.text("540")),
    )


def downgrade() -> None:
    op.drop_table("users")
