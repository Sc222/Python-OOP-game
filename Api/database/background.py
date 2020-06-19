from peewee import *
from database.level import Level
from app import db


class Background(db.Model):
    levelId = ForeignKeyField(Level, backref='backgrounds')
    type = IntegerField()
    x = IntegerField()
    y = IntegerField()

    class Meta:
        table_name = 'backgrounds'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
