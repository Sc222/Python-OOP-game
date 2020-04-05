from peewee import *
from main.monster import Monster


class MonsterInfo(Model):
    type = ForeignKeyField(Monster, backref='monstersInfo')
    image = TextField()  # путь до картинки (картинки будут храниться локально)
    hp = IntegerField()
    attack = IntegerField()
    defence = IntegerField()

    class Meta:
        table_name = 'monstersInfo'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
