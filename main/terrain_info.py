from peewee import *
from main.background import Background


class TerrainInfo(Model):
    type = ForeignKeyField(Background, backref='terrainsInfo')
    image = TextField()  # путь до картинки (картинки будут храниться локально)

    class Meta:
        table_name = 'terrainsInfo'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
