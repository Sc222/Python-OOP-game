from peewee import *
from app import db

class BackgroundInfo(db.Model):
    image = TextField()  # путь до картинки (картинки будут храниться локально)

    class Meta:
        table_name = 'backgroundsInfo'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
