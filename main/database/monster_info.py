from peewee import *


class MonsterInfo(Model):
    image = TextField()  # путь до картинки (картинки будут храниться локально)
    hp = IntegerField()
    attack = IntegerField()
    defence = IntegerField()

    class Meta:
        table_name = 'monstersInfo'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
