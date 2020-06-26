"""empty message

Revision ID: 879bb3e69938
Revises: 5682c771c2fd
Create Date: 2020-06-27 01:31:31.223189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '879bb3e69938'
down_revision = '5682c771c2fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('background_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('leaderboard_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('playerName', sa.String(), nullable=True),
    sa.Column('levelId', sa.Integer(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('level',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sizeX', sa.Integer(), nullable=True),
    sa.Column('sizeY', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('monster_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=True),
    sa.Column('attack', sa.Integer(), nullable=True),
    sa.Column('defence', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('terrain_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('unlockedLevel', sa.Integer(), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=True),
    sa.Column('attack', sa.Integer(), nullable=True),
    sa.Column('defence', sa.Integer(), nullable=True),
    sa.Column('playerLevel', sa.Integer(), nullable=True),
    sa.Column('xp', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nickname')
    )
    op.create_table('background',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level_id', sa.Integer(), nullable=True),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.Column('infoId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['infoId'], ['background_info.id'], ),
    sa.ForeignKeyConstraint(['level_id'], ['level.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('monster',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('levelId', sa.Integer(), nullable=True),
    sa.Column('infoId', sa.Integer(), nullable=True),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['infoId'], ['monster_info.id'], ),
    sa.ForeignKeyConstraint(['levelId'], ['level.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('terrain',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('levelId', sa.Integer(), nullable=True),
    sa.Column('infoId', sa.Integer(), nullable=True),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['infoId'], ['terrain_info.id'], ),
    sa.ForeignKeyConstraint(['levelId'], ['level.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('terrain')
    op.drop_table('monster')
    op.drop_table('background')
    op.drop_table('user')
    op.drop_table('terrain_info')
    op.drop_table('monster_info')
    op.drop_table('level')
    op.drop_table('leaderboard_record')
    op.drop_table('background_info')
    # ### end Alembic commands ###
