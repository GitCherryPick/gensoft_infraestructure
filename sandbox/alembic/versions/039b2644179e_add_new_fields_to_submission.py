"""Add new fields to submission

Revision ID: 039b2644179e
Revises: 3d0b2e68cb3f
Create Date: 2025-06-01 23:25:27.331996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '039b2644179e'
down_revision: Union[str, None] = '3d0b2e68cb3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('submissions', sa.Column('is_autogenerated', sa.Boolean(), nullable=True))
    op.add_column('submissions', sa.Column('autofeedback_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('submissions', 'autofeedback_id')
    op.drop_column('submissions', 'is_autogenerated')
    # ### end Alembic commands ###
