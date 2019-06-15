"""create contestant table

Revision ID: 3a3c438bb577
Revises: 587902e2dda2
Create Date: 2019-06-15 20:37:34.882301

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3a3c438bb577'
down_revision = '587902e2dda2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contestant_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=16), nullable=False),
    sa.Column('gender', mysql.ENUM('male', 'female'), nullable=False),
    sa.Column('birth', sa.DateTime(), nullable=False),
    sa.Column('agent_phone', sa.String(length=16), nullable=False),
    sa.Column('phone', sa.String(length=16), nullable=False),
    sa.Column('school', sa.String(length=64), nullable=True),
    sa.Column('grade', sa.Integer(), nullable=True),
    sa.Column('klass', sa.Integer(), nullable=True),
    sa.Column('zip_code', sa.String(length=8), nullable=False),
    sa.Column('address', sa.String(length=128), nullable=False),
    sa.Column('detail_address', sa.String(length=128), nullable=False),
    sa.Column('sector', mysql.ENUM('programming', 'design', 'business'), nullable=False),
    sa.Column('photo', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('launch_number', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contestant_model')
    # ### end Alembic commands ###
