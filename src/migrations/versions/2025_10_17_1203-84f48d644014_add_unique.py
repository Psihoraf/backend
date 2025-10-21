"""add unique

Revision ID: 84f48d644014
Revises: d8bdc211eb6d
Create Date: 2025-10-17 12:03:50.890101

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "84f48d644014"
down_revision: Union[str, Sequence[str], None] = "d8bdc211eb6d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("users_email_key", "users", ["email"])


def downgrade() -> None:
    op.drop_constraint("users_email_key", "users", type_="unique")
