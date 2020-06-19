from peewee import *


class TerrainInfo(Model):
    image = TextField()  # путь до картинки (картинки будут храниться локально)

    class Meta:
        table_name = 'terrainsInfo'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
