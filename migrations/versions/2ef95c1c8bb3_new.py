"""new. Add new column in User "is_verifed"

Revision ID: 2ef95c1c8bb3
Revises: 655c0c342056
Create Date: 2025-01-31 20:10:01.640124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ef95c1c8bb3'
down_revision: Union[str, None] = '655c0c342056'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'urls', ['id'])
    op.add_column('users', sa.Column('is_verifed', sa.Boolean(), default=False))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'is_verifed')
    op.drop_constraint(None, 'urls', type_='unique')
    # ### end Alembic commands ###
