from peewee import *
from main.level import Level


class Terrain(Model):
    levelId = ForeignKeyField(Level, backref='terrains')
    type = TextField()
    x = IntegerField()
    y = IntegerField()

    class Meta:
        table_name = 'terrains'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
