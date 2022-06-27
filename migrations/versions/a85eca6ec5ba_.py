"""empty message

Revision ID: a85eca6ec5ba
Revises: 284ab2fdeedc
Create Date: 2022-06-27 10:51:28.935068

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a85eca6ec5ba'
down_revision = '284ab2fdeedc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('db_user', 'account')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db_user', sa.Column('account', mysql.VARCHAR(length=255), nullable=False))
    # ### end Alembic commands ###