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

    def __init__(self, nickname, password):
        self.nickname = nickname
        self.password = password
        self.unlockedLevel = 0
        self.hp = 100
        self.attack = 50
        self.defence = 0
        self.playerLevel = 1
        self.xp = 0

    class Meta:
        table_name = 'players'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
