from main.background import Background
from main.terrain import Terrain
from main.monster import Monster
from main.background_info import BackgroundInfo
from main.terrain_info import TerrainInfo
from main.monster_info import MonsterInfo
from main.leaderboard_record import LeaderboardRecord
from main.player import Player
from main.level import Level


# здесь будут методы для работы с базой данных
class Dbhelper1():

    def RegisterUser(self,userName, password):
        player = Player(userName, password)
        player.save()

    def GetUser(self,userName,password):
        players = Player.select().where(Player.nickname == userName)
        player = players[0]
        return player

    def GetLevel(self,levelId):
        level = Level.select().where(Level.id==levelId)
        #я хуй его знает