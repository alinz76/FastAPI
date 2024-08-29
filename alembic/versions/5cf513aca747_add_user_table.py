"""add user table

Revision ID: 5cf513aca747
Revises: c958bf04fa98
Create Date: 2024-08-20 22:40:56.306971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cf513aca747'
down_revision: Union[str, None] = 'c958bf04fa98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts2', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts2', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='post2')
    op.drop_column('posts2', 'owner_id')