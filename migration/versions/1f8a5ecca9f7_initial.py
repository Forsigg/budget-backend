"""initial

Revision ID: 1f8a5ecca9f7
Revises: 
Create Date: 2023-01-22 02:50:38.219326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f8a5ecca9f7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('budget_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=40), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_budget_user_id'), 'budget_user', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_budget_user_id'), table_name='budget_user')
    op.drop_table('budget_user')
    # ### end Alembic commands ###
