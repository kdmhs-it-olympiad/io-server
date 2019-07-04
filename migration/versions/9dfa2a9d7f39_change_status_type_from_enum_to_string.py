"""change status type from enum to string

Revision ID: 9dfa2a9d7f39
Revises: ca80e269779f
Create Date: 2019-07-04 23:24:34.990482

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9dfa2a9d7f39'
down_revision = 'ca80e269779f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('calender_model', 'status',
               existing_type=mysql.VARCHAR(length=64), nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('calender_model', 'status',
               existing_type=mysql.ENUM('applying', 'design_1st_submitting', 'design_1st_announcing', 'waiting_for_contest', 'contesting', 'final_submitting', 'end'),
               nullable=True)
    # ### end Alembic commands ###
