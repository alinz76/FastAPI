"""added creating column to posts table

Revision ID: 0591c9234cd2
Revises: 5cf513aca747
Create Date: 2024-08-21 01:20:18.783148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0591c9234cd2'
down_revision: Union[str, None] = '5cf513aca747'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts2', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column('posts2', 'created_at')
