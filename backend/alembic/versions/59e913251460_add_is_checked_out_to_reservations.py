"""add_is_checked_out_to_reservations

Revision ID: 59e913251460
Revises: a7038db1f3eb
Create Date: 2024-10-30 12:44:06.429196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59e913251460'
down_revision: Union[str, None] = 'a7038db1f3eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_tools_category', table_name='tools')
    op.drop_index('ix_tools_id', table_name='tools')
    op.drop_index('ix_tools_name', table_name='tools')
    op.drop_table('tools')
    op.drop_index('ix_reservations_id', table_name='reservations')
    op.drop_table('reservations')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=1)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=1)
    op.create_table('reservations',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('tool_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('reservation_date', sa.DATE(), nullable=False),
    sa.Column('return_date', sa.DATE(), nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['tool_id'], ['tools.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_reservations_id', 'reservations', ['id'], unique=False)
    op.create_table('tools',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('category', sa.VARCHAR(), nullable=True),
    sa.Column('owner_id', sa.INTEGER(), nullable=True),
    sa.Column('is_available', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tools_name', 'tools', ['name'], unique=False)
    op.create_index('ix_tools_id', 'tools', ['id'], unique=False)
    op.create_index('ix_tools_category', 'tools', ['category'], unique=False)
    # ### end Alembic commands ###
