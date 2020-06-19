from peewee import *
from database.level import Level


class Monster(Model):
    levelId = ForeignKeyField(Level, backref='monsters')
    type = IntegerField()
    x = IntegerField()
    y = IntegerField()

    class Meta:
        table_name = 'monsters'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
