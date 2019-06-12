"""create calender table

Revision ID: 1fdce8ac3742
Revises: 
Create Date: 2019-06-12 20:33:59.205633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fdce8ac3742'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('calender_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('context', sa.Integer(), nullable=True),
    sa.Column('begin', sa.DateTime(), nullable=False),
    sa.Column('end', sa.DateTime(), nullable=False),
    sa.Column('visable', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('calender_model')
    # ### end Alembic commands ###
