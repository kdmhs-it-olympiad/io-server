"""currect the qa table

Revision ID: 9d345423f235
Revises: fc638e54c2a1
Create Date: 2019-06-20 22:51:05.580488

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9d345423f235'
down_revision = 'fc638e54c2a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contestant_model', 'photo',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.add_column('qa_model', sa.Column('answer', sa.Text(), nullable=True))
    op.add_column('qa_model', sa.Column('question', sa.Text(), nullable=False))
    op.drop_column('qa_model', 'context')
    op.drop_column('qa_model', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('qa_model', sa.Column('title', mysql.VARCHAR(length=256), nullable=False))
    op.add_column('qa_model', sa.Column('context', mysql.TEXT(), nullable=False))
    op.drop_column('qa_model', 'question')
    op.drop_column('qa_model', 'answer')
    op.alter_column('contestant_model', 'photo',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    # ### end Alembic commands ###
