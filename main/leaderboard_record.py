from peewee import *
from main.player import Player


class LeaderboardRecord(Model):
    playerId = ForeignKeyField(Player, backref='leaderboards')
    levelId = IntegerField()
    score = IntegerField()

    class Meta:
        table_name = 'leaderboards'
        database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
