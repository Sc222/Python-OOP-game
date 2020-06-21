from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
leaderboard_record = Table('leaderboard_record', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('playerId', Integer),
    Column('levelId', Integer),
    Column('score', Integer),
)

player = Table('player', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String),
    Column('password', String),
    Column('unlockedLevel', Integer),
    Column('hp', Integer),
    Column('attack', Integer),
    Column('defence', Integer),
    Column('playerLevel', Integer),
    Column('xp', Integer),
)

terrain = Table('terrain', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('levelId', Integer),
    Column('infoId', Integer),
    Column('x', Integer),
    Column('y', Integer),
)

terrain_info = Table('terrain_info', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('image', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['leaderboard_record'].create()
    post_meta.tables['player'].create()
    post_meta.tables['terrain'].create()
    post_meta.tables['terrain_info'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['leaderboard_record'].drop()
    post_meta.tables['player'].drop()
    post_meta.tables['terrain'].drop()
    post_meta.tables['terrain_info'].drop()
