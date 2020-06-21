from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
background_info = Table('background_info', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('imageSource', String),
)

monster = Table('monster', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('levelId', Integer),
    Column('infoId', Integer),
    Column('x', Integer),
    Column('y', Integer),
)

monster_info = Table('monster_info', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('image_source', String),
    Column('hp', Integer),
    Column('attack', Integer),
    Column('defence', Integer),
)

background = Table('background', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('level_id', INTEGER),
    Column('type', INTEGER),
    Column('x', INTEGER),
    Column('y', INTEGER),
    Column('image', VARCHAR),
)

background = Table('background', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('level_id', Integer),
    Column('x', Integer),
    Column('y', Integer),
    Column('infoId', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['background_info'].create()
    post_meta.tables['monster'].create()
    post_meta.tables['monster_info'].create()
    pre_meta.tables['background'].columns['image'].drop()
    pre_meta.tables['background'].columns['type'].drop()
    post_meta.tables['background'].columns['infoId'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['background_info'].drop()
    post_meta.tables['monster'].drop()
    post_meta.tables['monster_info'].drop()
    pre_meta.tables['background'].columns['image'].create()
    pre_meta.tables['background'].columns['type'].create()
    post_meta.tables['background'].columns['infoId'].drop()
