"""Prueba

Revision ID: ebb49bd45fb4
Revises: 8d93325e9081
Create Date: 2025-06-08 00:08:03.866735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ebb49bd45fb4'
down_revision: Union[str, None] = '8d93325e9081'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('used_hints',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('task_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('hint_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('used_at', mysql.DATETIME(), server_default=sa.text('(now())'), nullable=True),
    sa.ForeignKeyConstraint(['hint_id'], ['hints.hint_id'], name='used_hints_ibfk_2'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='used_hints_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('uq_user_task_hint', 'used_hints', ['user_id', 'task_id', 'hint_id'], unique=True)
    op.create_index('ix_used_hints_id', 'used_hints', ['id'], unique=False)
    # ### end Alembic commands ###
