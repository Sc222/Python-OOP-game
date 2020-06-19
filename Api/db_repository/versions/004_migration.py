from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
background = Table('background', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('level_id', Integer),
    Column('type', Integer),
    Column('x', Integer),
    Column('y', Integer),
)

level = Table('level', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('sizeX', Integer),
    Column('sizeY', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['background'].create()
    post_meta.tables['level'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['background'].drop()
    post_meta.tables['level'].drop()
