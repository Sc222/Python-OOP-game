"""empty message

Revision ID: 5682c771c2fd
Revises: b0bc70112650
Create Date: 2020-06-26 02:34:25.609417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5682c771c2fd'
down_revision = 'b0bc70112650'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.String(), nullable=True))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(), nullable=True))
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###
