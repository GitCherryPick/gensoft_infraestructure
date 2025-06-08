"""check_current_state

Revision ID: 61ab3b6b1269
Revises: a447d9569314
Create Date: 2025-06-08 01:07:50.588861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61ab3b6b1269'
down_revision: Union[str, None] = 'a447d9569314'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
