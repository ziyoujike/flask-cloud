"""empty message

Revision ID: 284ab2fdeedc
Revises: 42016723d7f4
Create Date: 2022-06-27 10:50:31.598017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '284ab2fdeedc'
down_revision = '42016723d7f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db_user', sa.Column('account', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('db_user', 'account')
    # ### end Alembic commands ###
