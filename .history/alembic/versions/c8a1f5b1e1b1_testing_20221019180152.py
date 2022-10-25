"""testing

Revision ID: c8a1f5b1e1b1
Revises: 2c23687dc95e
Create Date: 2022-10-19 18:00:15.622817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8a1f5b1e1b1'
down_revision = '2c23687dc95e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=function false at 0x000002B748620700 >))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###