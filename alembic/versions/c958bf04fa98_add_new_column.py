"""add new column

Revision ID: c958bf04fa98
Revises: 4b58bd618bf8
Create Date: 2024-08-20 22:33:55.468495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c958bf04fa98'
down_revision: Union[str, None] = '4b58bd618bf8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts2', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts2', 'content')
