from peewee import *
from main.background import Background


class BackgroundInfo(Model):
    type = ForeignKeyField(Background, backref='backgroundsInfo')
    image = TextField()  # путь до картинки (картинки будут храниться локально)

    class Meta:
        table_name = 'backgroundsInfo'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
