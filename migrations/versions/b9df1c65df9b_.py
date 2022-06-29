"""empty message

Revision ID: b9df1c65df9b
Revises: 59c7e4dd0f0d
Create Date: 2022-06-28 17:04:44.007624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9df1c65df9b'
down_revision = '59c7e4dd0f0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('db_collection_resources',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('resources_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['resources_id'], ['db_resources.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['db_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('db_collection_resources')
    # ### end Alembic commands ###
