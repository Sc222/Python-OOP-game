from peewee import *


class BackgroundInfo(Model):
    image = TextField()  # путь до картинки (картинки будут храниться локально)

    class Meta:
        table_name = 'backgroundsInfo'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
