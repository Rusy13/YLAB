"""initial2

Revision ID: e46f0efb2447
Revises: 45b9ad6674e2
Create Date: 2024-01-25 20:31:36.576172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e46f0efb2447'
down_revision: Union[str, None] = '45b9ad6674e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menus',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_menus_title'), 'menus', ['title'], unique=False)
    op.create_table('submenus',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('menu_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_submenus_title'), 'submenus', ['title'], unique=False)
    op.create_table('dishes',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.String(), nullable=True),
    sa.Column('submenu_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['submenu_id'], ['submenus.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_dishes_title'), 'dishes', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dishes_title'), table_name='dishes')
    op.drop_table('dishes')
    op.drop_index(op.f('ix_submenus_title'), table_name='submenus')
    op.drop_table('submenus')
    op.drop_index(op.f('ix_menus_title'), table_name='menus')
    op.drop_table('menus')
    # ### end Alembic commands ###