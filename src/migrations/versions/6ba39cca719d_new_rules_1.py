"""new rules #1

Revision ID: 6ba39cca719d
Revises: f6d034fbfaeb
Create Date: 2024-06-05 18:48:01.108822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ba39cca719d'
down_revision: Union[str, None] = 'f6d034fbfaeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reports', 'place_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('reports', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reports', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('reports', 'place_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
