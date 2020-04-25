from peewee import *


class Player(Model):
    nickname = TextField(unique=True)
    password = TextField()  # хранится не пароль, а его хэш
    unlockedLevel = IntegerField()  # максимальный разблок. уровень
    hp = IntegerField()
    attack = IntegerField()
    defence = IntegerField()
    playerLevel = IntegerField()
    xp = IntegerField()  # сколько опыта получено с пред. уровня

    class Meta:
        table_name = 'players'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
