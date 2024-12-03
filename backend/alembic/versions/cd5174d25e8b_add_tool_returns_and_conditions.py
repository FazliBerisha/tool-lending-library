"""add tool returns and conditions

Revision ID: cd5174d25e8b
Revises: 63ef2524a0df
Create Date: 2024-12-02 21:39:11.588677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd5174d25e8b'
down_revision: Union[str, None] = '63ef2524a0df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_tools_id', table_name='tools')
    op.drop_table('tools')
    op.drop_index('ix_reservations_id', table_name='reservations')
    op.drop_table('reservations')
    op.drop_index('ix_tool_submissions_id', table_name='tool_submissions')
    op.drop_table('tool_submissions')
    op.drop_index('ix_tool_returns_id', table_name='tool_returns')
    op.drop_table('tool_returns')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tool_returns',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('reservation_id', sa.INTEGER(), nullable=True),
    sa.Column('condition', sa.VARCHAR(length=9), nullable=True),
    sa.Column('damages', sa.VARCHAR(), nullable=True),
    sa.Column('return_reason', sa.VARCHAR(), nullable=True),
    sa.Column('feedback', sa.VARCHAR(), nullable=True),
    sa.Column('return_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['reservation_id'], ['reservations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tool_returns_id', 'tool_returns', ['id'], unique=False)
    op.create_table('tool_submissions',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('category', sa.VARCHAR(), nullable=True),
    sa.Column('condition', sa.VARCHAR(), nullable=True),
    sa.Column('image_url', sa.VARCHAR(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('status', sa.VARCHAR(), nullable=True),
    sa.Column('submitted_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tool_submissions_id', 'tool_submissions', ['id'], unique=False)
    op.create_table('reservations',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('tool_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('reservation_date', sa.DATE(), nullable=False),
    sa.Column('return_date', sa.DATE(), nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), nullable=True),
    sa.Column('is_checked_out', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['tool_id'], ['tools.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_reservations_id', 'reservations', ['id'], unique=False)
    op.create_table('tools',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('category', sa.VARCHAR(), nullable=True),
    sa.Column('owner_id', sa.INTEGER(), nullable=True),
    sa.Column('is_available', sa.BOOLEAN(), nullable=True),
    sa.Column('condition', sa.VARCHAR(), nullable=True),
    sa.Column('image_url', sa.VARCHAR(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tools_id', 'tools', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), nullable=True),
    sa.Column('role', sa.VARCHAR(length=5), nullable=True),
    sa.Column('full_name', sa.VARCHAR(), nullable=True),
    sa.Column('bio', sa.VARCHAR(), nullable=True),
    sa.Column('location', sa.VARCHAR(), nullable=True),
    sa.Column('profile_picture', sa.VARCHAR(), nullable=True),
    sa.Column('profile_image_url', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=1)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=1)
    # ### end Alembic commands ###
