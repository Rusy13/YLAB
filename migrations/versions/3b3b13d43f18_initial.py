"""initial

Revision ID: 3b3b13d43f18
Revises: 
Create Date: 2024-01-21 21:01:08.674505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b3b13d43f18'
down_revision: Union[str, None] = None
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
