from peewee import *


class Level(Model):
    # !!! поле id сгенерируется само
    sizeX = IntegerField()
    sizeY = IntegerField()

    class Meta:
        table_name = 'levels'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
