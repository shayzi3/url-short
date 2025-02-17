"""new. Add new Table 'ApiKey'

Revision ID: 4d0aca94bccf
Revises: bf2984b052bf
Create Date: 2025-02-04 17:13:34.567714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.core.security import generate_prefix


# revision identifiers, used by Alembic.
revision: str = '4d0aca94bccf'
down_revision: Union[str, None] = 'bf2984b052bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('keys',
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('exp', sa.Float(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_name'], ['users.username'], ),
    sa.PrimaryKeyConstraint('key'),
    sa.UniqueConstraint('key')
    )
    op.alter_column('users', 'is_verifed',
               existing_type=sa.BOOLEAN(),
               default=False)
    op.alter_column('users', 'is_banned',
               existing_type=sa.BOOLEAN(),
               default=False)
    op.alter_column('users', 'prefix',
               existing_type=sa.VARCHAR(),
               default=generate_prefix())
    op.drop_column('users', 'api_key')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('api_key', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('users', 'prefix',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'is_banned',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('users', 'is_verifed',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_table('keys')
    # ### end Alembic commands ###
