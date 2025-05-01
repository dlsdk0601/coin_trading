"""add_manager_table

Revision ID: 019fd892494f
Revises: 84d37111ecd9
Create Date: 2025-05-01 21:50:24.213475

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '019fd892494f'
down_revision: Union[str, None] = '84d37111ecd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('manager',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('id', sa.String(length=32), nullable=False, comment='로그인 아이디'),
                    sa.Column('password_hash', sa.String(length=512), nullable=False, comment='로그인 비밀번호 해쉬'),
                    sa.Column('create_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False,
                              comment='생성 일자'),
                    sa.Column('update_at', sa.DateTime(timezone=True), nullable=True, comment='수정 일자'),
                    sa.Column('delete_at', sa.DateTime(timezone=True), nullable=True, comment='삭제 일자'),
                    sa.PrimaryKeyConstraint('pk'),
                    comment='관리자'
                    )
    op.create_table('manager_authentication',
                    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('create_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False,
                              comment='생성 일자'),
                    sa.Column('update_at', sa.DateTime(timezone=True), nullable=True, comment='수정 일자'),
                    sa.Column('manager_pk', sa.Integer(), nullable=False),
                    sa.Column('access_token', sa.UUID(), nullable=False, comment='토큰'),
                    sa.Column('expired_at', sa.DateTime(timezone=True), nullable=False, comment='만료 일자'),
                    sa.ForeignKeyConstraint(['manager_pk'], ['manager.pk'], ),
                    sa.PrimaryKeyConstraint('pk'),
                    sa.UniqueConstraint('access_token'),
                    comment='관리자 - Authentication'
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('manager_authentication')
    op.drop_table('manager')
