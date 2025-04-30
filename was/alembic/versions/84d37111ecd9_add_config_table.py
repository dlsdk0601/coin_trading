"""add_config_table

Revision ID: 84d37111ecd9
Revises: 
Create Date: 2025-05-01 03:50:47.530943

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '84d37111ecd9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('config',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('key', sa.String(length=64), nullable=False, comment='key'),
                    sa.Column('value', sa.String(length=64), nullable=False, comment='value'),
                    sa.Column('create_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.Column('update_at', sa.DateTime(timezone=True), nullable=True),
                    sa.PrimaryKeyConstraint('pk'),
                    sa.UniqueConstraint('key'),
                    comment='환경 변수'
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('config')
