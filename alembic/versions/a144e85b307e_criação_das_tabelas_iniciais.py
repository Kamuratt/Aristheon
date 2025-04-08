"""criação das tabelas iniciais

Revision ID: a144e85b307e
Revises: 
Create Date: 2025-04-08 08:03:39.618346
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql  # IMPORTANTE


# revision identifiers, used by Alembic.
revision: str = 'a144e85b307e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ✅ Criação segura dos ENUMs
    userrole_enum = postgresql.ENUM('OPERATOR', 'BUYER', 'MANAGER', name='userrole')
    userrole_enum.create(op.get_bind(), checkfirst=True)

    prstatus_enum = postgresql.ENUM('PENDING', 'APPROVED', 'REJECTED', name='prstatus')
    prstatus_enum.create(op.get_bind(), checkfirst=True)

    # ✅ Tabelas com ENUM já existente (create_type=False)
    op.create_table('products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('current_stock', sa.Integer(), nullable=False),
        sa.Column('min_stock', sa.Integer(), server_default='0', nullable=False),
        sa.Column('max_stock', sa.Integer(), server_default='1', nullable=False),
        sa.CheckConstraint('current_stock >= 0', name='check_current_stock_non_negative'),
        sa.CheckConstraint('max_stock > min_stock', name='check_max_stock_greater'),
        sa.CheckConstraint('min_stock >= 0', name='check_min_stock_non_negative'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_product_stocks', 'products', ['min_stock', 'max_stock'], unique=False)
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_index(op.f('ix_products_name'), 'products', ['name'], unique=False)

    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=256), nullable=False),
        sa.Column('role', sa.Enum('OPERATOR', 'BUYER', 'MANAGER', name='userrole', create_type=False), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    op.create_table('purchase_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), server_default='1', nullable=False),
        sa.Column('requester_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='prstatus', create_type=False), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.CheckConstraint('quantity > 0', name='check_quantity_positive'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['requester_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchase_requests_created_at'), 'purchase_requests', ['created_at'], unique=False)
    op.create_index(op.f('ix_purchase_requests_id'), 'purchase_requests', ['id'], unique=False)
    op.create_index(op.f('ix_purchase_requests_status'), 'purchase_requests', ['status'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_purchase_requests_status'), table_name='purchase_requests')
    op.drop_index(op.f('ix_purchase_requests_id'), table_name='purchase_requests')
    op.drop_index(op.f('ix_purchase_requests_created_at'), table_name='purchase_requests')
    op.drop_table('purchase_requests')

    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

    op.drop_index(op.f('ix_products_name'), table_name='products')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_index('idx_product_stocks', table_name='products')
    op.drop_table('products')

    # ✅ Drop dos ENUMs
    prstatus_enum = postgresql.ENUM(name='prstatus')
    prstatus_enum.drop(op.get_bind(), checkfirst=True)

    userrole_enum = postgresql.ENUM(name='userrole')
    userrole_enum.drop(op.get_bind(), checkfirst=True)
