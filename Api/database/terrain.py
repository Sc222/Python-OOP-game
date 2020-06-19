from peewee import *
from database.level import Level


class Terrain(Model):
    levelId = ForeignKeyField(Level, backref='terrains')
    type = IntegerField()
    x = IntegerField()
    y = IntegerField()

    class Meta:
        table_name = 'terrains'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
