from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
leaderboard_record = Table('leaderboard_record', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('playerId', INTEGER),
    Column('levelId', INTEGER),
    Column('score', INTEGER),
)

leaderboard_record = Table('leaderboard_record', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('playerName', String),
    Column('levelId', Integer),
    Column('score', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['leaderboard_record'].columns['playerId'].drop()
    post_meta.tables['leaderboard_record'].columns['playerName'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['leaderboard_record'].columns['playerId'].create()
    post_meta.tables['leaderboard_record'].columns['playerName'].drop()
